# coding: utf8
from __future__ import unicode_literals
import scrapy
from scrapy.http import Request

from app_spider.items import ApkDetailItem
from store.models import AppInfo


class CoolApkDetailSpider(scrapy.Spider):
    name = 'coolapk_detail'
    allowed_domains = ['coolapk.com']
    start_url_format = "http://coolapk.com/apk/%s"

    # xpath
    score_xpath = """
    //div[@id='ex-apk-rank-pane' and @class='tab-pane active ex-apk-rank-pane']/div[1][@class='media ex-apk-rank']/div[@class='pull-left ex-apk-rank-intro']/span[2][@class='ex-apk-rank-score']/text()
    """
    detail_key_xpath = """
    //div[@id='ex-apk-detail-pane' and @class='tab-pane ex-apk-detail-pane']/dl[@class='dl-horizontal']/dt//text()
    """
    detail_val_xpath = """
    //div[@id='ex-apk-detail-pane' and @class='tab-pane ex-apk-detail-pane']/dl[@class='dl-horizontal']/dd//text()
    """
    permission_name_xpath = "//div[@id='ex-apk-permission-pane' and @class='tab-pane ex-apk-permission-pane']/dl[@class='dl-horizontal']/dt//text()"
    permission_desc_xpath = "//div[@id='ex-apk-permission-pane' and @class='tab-pane ex-apk-permission-pane']/dl[@class='dl-horizontal']/dd//strong/text()"
    tags_xpath = """
    /html/body/div[3][@class='container ex-container']/div[@class='row']/div[1][@class='col-md-5']/div[5][@class='panel panel-default ex-card']/div[@class='panel-body']/a//text()
    """
    intro_xpath = """
    /html/body/div[3][@class='container ex-container']/div[@class='row']/div[1][@class='col-md-5']/div[6][@class='panel panel-default ex-card']/div[2][@class='ex-card-content']//text()
    """
    logo_xpath = """
    /html/body/div[2][@class='ex-page-header']/div[@class='container']/div[1][@class='media ex-page-topbar']/a[@class='pull-left ex-apk-view-logo']/img/@src
    """
    screenshot_xpath = "//div[@id='ex-screenshot-carousel' and @class='carousel slide ex-screenshot-carousel']/div[@class='carousel-inner']//img/@src"

    def __init__(self, apk_name=None, *args, **kwargs):
        super(CoolApkDetailSpider, self).__init__(*args, **kwargs)
        self.apk_name = apk_name

    def start_requests(self):
        """
        如果指定了self.apk_name, 则只抓取某一个app
        """
        if self.apk_name:
            yield Request(self.start_url_format % self.apk_name)
        else:
            # TODO: 把model-instance传递下去,这样在pipeline中,减少对数据库的访问
            apk_names_to_crawl = AppInfo.objects.filter(is_crawled__exact=0).values_list('apk_name', flat=True)
            for apk_name in apk_names_to_crawl:
                yield Request(self.start_url_format % apk_name)

    def parse(self, response):
        item = ApkDetailItem()
        item['apk_name'] = response.url.split('/')[-1]
        item['score'] = response.xpath(self.score_xpath).extract()[0]
        # TODO: download_url
        # ...
        # details
        keys = response.xpath(self.detail_key_xpath).extract()
        keys = [key[:-1] for key in keys]
        vals = response.xpath(self.detail_val_xpath).extract()
        item['details'] = dict(zip(keys, vals))
        # permission
        names = response.xpath(self.permission_name_xpath).extract()
        descs = response.xpath(self.permission_desc_xpath).extract()
        for i in range(len(names)-len(descs)):
            descs.append("")
        item['permissions'] = zip(names, descs)
        # category and tags
        tags = response.xpath(self.tags_xpath).extract()
        item['category'] = tags[0]
        item['tags'] = tags[1:]
        # intro
        item['intro'] = ''.join(response.xpath(self.intro_xpath).extract())
        # logo
        item['logo'] = {'url': response.xpath(self.logo_xpath).extract()[0], 'path': ''}
        # screenshots
        item['screenshots'] = [{'url': url, 'path': ''} for url in response.xpath(self.screenshot_xpath).extract()]
        yield item
