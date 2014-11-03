# coding: utf8
from __future__ import unicode_literals
from datetime import date

from app_spider.spiders.app_detail_base_spider import AppDetailBaseSpider
from store.models import AppInfo


class WandoujiaDetailSpider(AppDetailBaseSpider):
    name = 'wandoujia_detail'
    allowed_domains = ['http://www.wandoujia.com/']
    app_detail_url_format = "http://www.wandoujia.com/apps/%s"
    data_source = AppInfo.WANDOUJIA
    # css selector
    css_logo_origin_url = "body > div.container > div.detail-wrap > div.detail-top.clearfix > div.app-icon > img::attr(src)"
    css_name = 'body > div.container > div.detail-wrap > div.detail-top.clearfix > div.app-info > p.app-name > span::text'
    css_download_url = 'body > div.container > div.detail-wrap > div.detail-top.clearfix > div.app-info > div > a.install-btn::attr(href)'
    css_screenshots = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-left > div.screenshot > div.j-scrollbar-wrap > div.view-box > div > img::attr(src)'
    css_intro = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-left > div.desc-info > div.con::text'
    css_size = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd:nth-child(2) > meta::attr(content)'
    css_last_version = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd:nth-child(8)::text'
    css_permissions_str = '#j-perms-list > li > span::text'
    css_rom = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd.perms::text'
    css_developer = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd:nth-child(12) > span:nth-child(1) > meta::attr(content)'
    css_update_date = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd:nth-child(6) > time::attr(datetime)'
    css_update_log = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-left > div.change-info > div.con::text'

    def start_requests(self):
        for req in super(WandoujiaDetailSpider, self).start_requests():
            req.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
            yield req

    def _parse(self, response):
        item = super(WandoujiaDetailSpider, self)._parse(response)
        instance = response.meta['instance']
        tags_css = 'body > div.container > div.detail-wrap > div:nth-child(2) > div.col-right > div > dl > dd.tag-box > a::text'
        tags = response.css(tags_css).extract()
        item['category'] = tags[0]
        item['tags'] = tags[1:]
        item['instance'] = instance
        item['apk_name'] = response.meta['apk_name']
        item['data_source'] = AppInfo.WANDOUJIA
        if item['update_date']:
            item['update_date'] = date(*[int(n) for n in item['update_date'].split('-')])
        return item
