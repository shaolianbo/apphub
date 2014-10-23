# coding: utf8
from __future__ import unicode_literals
import json

import scrapy
from scrapy.http import Request

from app_spider.items import AppIdentificationItem
from store.models import APP, GAME


class WandoujiaListSpider(scrapy.Spider):
    name = 'wandoujia_list'
    allowed_domains = ['apps.wandoujia.com', 'www.wandoujia.com']
    # 每次从接口最多拿60个app信息
    app_list_url_format = 'http://apps.wandoujia.com/api/v1/apps?tag=%s&max=60&start=%s&opt_fields=apps.packageName'

    def __init__(self, tag=None, top_type=APP, *args, **kwargs):
        super(WandoujiaListSpider, self).__init__(*args, **kwargs)
        self.tag = tag
        self.top_type = int(top_type)
        if self.tag:
            if not isinstance(self.tag, unicode):
                self.tag = self.tag.decode('utf8')

    def _package_name_request(self, tag, start, top_type):
        req = Request(self.app_list_url_format % (tag, start), callback=self.parse_package_name)
        req.meta['tag'] = tag
        req.meta['start'] = start
        req.meta['top_type'] = top_type
        return req

    def start_requests(self):
        if self.tag:
            yield self._package_name_request(self.tag, 1, self.top_type)
        else:
            app_req = Request("http://www.wandoujia.com/tag/app", callback=self.parse_tags)
            app_req.meta['top_type'] = APP
            yield app_req
            game_req = Request("http://www.wandoujia.com/tag/game", callback=self.parse_tags)
            game_req.meta['top_type'] = GAME
            yield game_req

    def parse_tags(self, response):
        css_str = "body > div.container > ul.clearfix.tag-box > li > a > span::text"
        tags = response.css(css_str).extract()
        top_type = response.meta['top_type']
        for tag in tags:
            yield self._package_name_request(tag, 1, top_type)

    def parse_package_name(self, response):
        # 如果抓取结果为404, 则表明抓取完成
        # 404的response会自动被scrapy的中间键过滤掉, 此处不做处理
        apps = json.loads(response.body)[0]['apps']
        top_type = response.meta['top_type']
        tag = response.meta['tag']
        for app in apps:
            item = AppIdentificationItem()
            item['apk_name'] = app['packageName']
            item['top_type'] = top_type
            item['category'] = tag
            yield item

        start = response.meta['start'] + 60
        yield self._package_name_request(tag, start, top_type)
