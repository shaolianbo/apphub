# coding: utf8
from __future__ import unicode_literals

import scrapy
from scrapy.http import Request
from scrapy import log

from app_spider.items import AppInfoItem
from store.models import AppInfo, AppIdentification


class WandoujiaDetailSpider(scrapy.Spider):
    name = 'wandoujia_detail'
    allowed_domains = ['http://www.wandoujia.com/']
    app_detail_url_format = "http://www.wandoujia.com/apps/%s"
    # css selector
    css_logo = "body > div.container > div.detail-wrap > div.detail-top.clearfix > div.app-icon > img::attr(src)"
    css_name = 'body > div.container > div.detail-wrap > div.detail-top.clearfix > div.app-info > p.app-name > span::text'
    css_download_url = 'body > div.container > div.detail-wrap > div.detail-top.clearfix > div.app-info > div > a.install-btn::attr(href)'
    css_screenshots = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-left > div.screenshot > div.j-scrollbar-wrap > div.view-box > div > img::attr(src)'
    css_intro = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-left > div.desc-info > div.con::text'
    css_size = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd::text'
    css_tags = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd.tag-box > a::text'
    css_version = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd:nth-child(8)::text'
    css_permissions = '#j-perms-list > li > span::text'
    css_rom = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd.perms::text'
    css_developer = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd:nth-child(12) > a > span::text'

    def __init__(self, apk_name=None, top_type=AppIdentification.APP, is_flush_db=False, *args, **kwargs):
        super(WandoujiaDetailSpider, self).__init__(*args, **kwargs)
        self.apk_name = apk_name
        self.top_type = top_type
        self.is_flush_db = bool(is_flush_db)

    def start_requests(self):
        if self.is_flush_db:
            # 根据AppIdentification 表, 在AppInfo中建立新的下载任务
            for app_id in AppIdentification.objects.all():
                appinfo, created = AppInfo.objects.get_or_create(
                    app_id_id=app_id.id,
                    data_source=AppInfo.WANDOUJIA
                )
            return
        if self.apk_name:
            app_id, created = AppIdentification.objects.get_or_create(
                apk_name=self.apk_name,
                top_type=self.top_type
            )
            appinfo, created = AppInfo.objects.get_or_create(
                app_id_id=app_id.id,
                data_source=AppInfo.WANDOUJIA
            )
            req = Request(self.app_detail_url_format % self.apk_name)
            req.meta['apk_name'] = self.apk_name
            req.meta['instance'] = appinfo
            yield req
        else:
            for appinfo in AppInfo.objects.filter(data_source=AppInfo.WANDOUJIA, is_crawled=False):
                req = Request(self.app_detail_url_format % appinfo.app_id.apk_name)
                req.meta['apk_name'] = appinfo.app_id.apk_name
                req.meta['instance'] = appinfo
                yield req

    def parse(self, response):
        item = AppInfoItem()
        item['instance'] = response.meta['instance']
        item['apk_name'] = response.meta['apk_name']
        item['data_source'] = AppInfo.WANDOUJIA
        item['logo'] = {'url': response.css(self.css_logo).extract()[0], 'path': ''}
        item['name'] = response.css(self.css_name).extract()[0]
        item['download_url'] = response.css(self.css_download_url).extract()[0]

        item['screenshots'] = []
        for shot in response.css(self.css_screenshots).extract():
            item['screenshots'].append({'url': shot, 'path': ''})

        item['intro'] = '<br>'.join(response.css(self.css_intro).extract())

        tags = response.css(self.css_tags).extract()
        item['category'] = tags[0]
        item['tags'] = tags[1:]

        item['permissions_str'] = ';'.join(response.css(self.css_permissions).extract())

        details = {}
        details['size'] = response.css(self.css_size).extract()[0].strip()
        details['last_version'] = response.css(self.css_version).extract()[0]
        details['rom'] = response.css(self.css_rom).extract()[0].strip()
        details['developer'] = response.css(self.css_developer).extract()[0]
        item['details'] = details

        yield item
