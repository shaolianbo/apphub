# coding: utf8
import scrapy
from scrapy.http import Request

from app_spider.items import ApkBaseItem


class CoolApkListSpider(scrapy.Spider):
    name = 'coolapk_list'
    allowed_domains = ['www.coolapk.com']
    start_urls = ['http://www.coolapk.com/apk/']
    app_list_url_format = "http://www.coolapk.com/apk/?p=%s"

    def parse(self, response):
        lastpage_xpath_str = """
        /html/body/div[4][@class='container ex-flex-container']/div[@class='row']/div[1][@class='col-md-8 ex-flex-col ']/div[@class='panel panel-default ex-card']/div[3][@class='panel-footer ex-card-footer text-center']/ul[@class='pagination']/li[11]/a/@href
        """
        last_page_url = response.xpath(lastpage_xpath_str).extract()[0]
        last_page_num = int(last_page_url.split("=")[-1])
        for page_num in range(1, last_page_num+1):
            yield Request(self.app_list_url_format % page_num, callback=self.list_parse)

    def list_parse(self, response):
        app_list_xpath_str = """
        /html/body/div[4][@class='container ex-flex-container']/div[@class='row']/div[1][@class='col-md-8 ex-flex-col ']/div[@class='panel panel-default ex-card']/div[2][@class='ex-card-body']/ul[@class='media-list ex-card-app-list']/li//h4/a
        """
        selectors = response.xpath(app_list_xpath_str)
        for selector in selectors:
            appitem = ApkBaseItem()
            appitem['name'] = selector.xpath('text()').extract()[0]
            appitem['apk_name'] = selector.xpath('@href').re(r'^/apk/(.*)')[0]
            yield appitem
