# coding: utf8
from __future__ import unicode_literals
import re

import scrapy
from scrapy.http import Request
from scrapy import log

from app_spider.items import AppInfoItemLoader, LackForFieldError
from store.models import AppIdentification, AppInfo


class AppDetailBaseSpider(scrapy.Spider):

    data_source = 0

    def __init__(self, apk_names=None, top_type=AppIdentification.APP, is_flush_db=False, *args, **kwargs):
        super(AppDetailBaseSpider, self).__init__(*args, **kwargs)
        self.apk_names = apk_names
        self.top_type = top_type
        self.is_flush_db = bool(is_flush_db)
        self.field_names_with_css = {}
        if self.apk_names:
            if type(self.apk_names) in (unicode, str):
                self.apk_names = self.apk_names.split(',')
        for name, attr in self.__class__.__dict__.items():
            match = re.match(r'css_(.+)', name)
            if match and not callable(attr):
                field_name = match.group(1)
                self.field_names_with_css[field_name] = attr

    def start_requests(self):
        if self.is_flush_db:
            # 根据AppIdentification 表, 在AppInfo中建立新的下载任务
            for app_id in AppIdentification.objects.all():
                appinfo, created = AppInfo.objects.get_or_create(
                    app_id_id=app_id.id,
                    data_source=self.data_source
                )
            return
        if self.apk_names:
            for apk_name in self.apk_names:
                app_id, created = AppIdentification.objects.get_or_create(
                    apk_name=apk_name,
                    top_type=self.top_type
                )
                appinfo, created = AppInfo.objects.get_or_create(
                    app_id_id=app_id.id,
                    data_source=self.data_source
                )
                req = Request(self.app_detail_url_format % apk_name)
                req.meta['apk_name'] = apk_name
                req.meta['instance'] = appinfo
                req.meta['dont_redirect'] = True
                yield req
        else:
            for appinfo in AppInfo.objects.filter(data_source=self.data_source, is_continue=True):
                req = Request(self.app_detail_url_format % appinfo.app_id.apk_name)
                req.meta['apk_name'] = appinfo.app_id.apk_name
                req.meta['instance'] = appinfo
                req.meta['dont_redirect'] = True
                yield req

    def _parse(self, response):
        loader = AppInfoItemLoader(response=response)
        for field_name, attr in self.field_names_with_css.items():
            loader.add_css(field_name, attr)
        item = loader.load_item()
        for name in self.field_names_with_css:
            if name not in item._values:
                self.log("(%s, %s, %s) css failed" % (self.__class__.__name__, name, response.url), log.ERROR)
        return item

    def parse(self, response):
        item = self._parse(response)
        if item:
            try:
                item.is_valid()
                yield item
            except LackForFieldError:
                raise
        else:
            return
