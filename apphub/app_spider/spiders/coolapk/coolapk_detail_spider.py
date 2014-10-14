# coding: utf8
from __future__ import unicode_literals
import re
import os

import scrapy
from scrapy.http import Request
from scrapy import log

from app_spider.items import AppInfoItem
from store.models import AppInfo


APK_DETAIL_VERBOSE_NAME_AND_FILED_NAME = {
    '软件名称': 'name',
    'APK名称': 'apk_name',
    '最新版本': 'last_version',
    '支持ROM': 'rom',
    '界面语言': 'language',
    '软件大小': 'size',
    '更新日期': 'update_time',
    '开发者': 'developer'
}


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

    download_xpath = "/html/body/script[1]/text()"

    def __init__(self, apk_name=None, is_download_package=False, *args, **kwargs):
        super(CoolApkDetailSpider, self).__init__(*args, **kwargs)
        self.apk_name = apk_name
        self.is_download_package = is_download_package

    def start_requests(self):
        """
        如果指定了self.apk_name, 则只抓取某一个app
        """
        if self.apk_name:
            try:
                apk = AppInfo.objects.get(apk_name=self.apk_name)
            except AppInfo.DoesNotExist:
                self.log("%s DoesNotExist in db" % self.apk_name, log.ERROR)
                return
            req = Request(self.start_url_format % self.apk_name)
            req.meta['instance'] = apk
            yield req
        else:
            apks_to_crawl = AppInfo.objects.filter(is_crawled__exact=0)
            for apk in apks_to_crawl:
                req = Request(self.start_url_format % apk.apk_name)
                req.meta['instance'] = apk
                yield req

    def parse(self, response):
        item = AppInfoItem()
        item['instance'] = response.meta['instance']
        item['apk_name'] = response.url.split('/')[-1]
        item['score'] = response.xpath(self.score_xpath).extract()[0]
        # TODO: item['name']
        # details
        keys = response.xpath(self.detail_key_xpath).extract()
        keys = [key[:-1] for key in keys]
        vals = response.xpath(self.detail_val_xpath).extract()
        details = dict(zip(keys, vals))
        item['details'] = {}
        for key, val in details.items():
            if key in APK_DETAIL_VERBOSE_NAME_AND_FILED_NAME:
                item['details'][APK_DETAIL_VERBOSE_NAME_AND_FILED_NAME[key]] = val
            else:
                log.msg('Unexpected detail key name %s' % key, level=log.WARNING)
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

        download_js = response.xpath(self.download_xpath).extract()[0].strip()
        download_url = 'http://coolapk.com' + re.match(r'.*apkDownloadUrl = "(.+)"', download_js).group(1)
        item['download_url'] = download_url
        yield item
        # downLoad pakage
        if self.is_download_package:
            download_req = Request(download_url, callback=self.complete_download)
            download_req.meta['instance'] = item['instance']
            yield download_req

    def complete_download(self, response):
        apk = response.meta['instance']
        if response.status != 200:
            self.log("%s package download failed: %s" % (apk, response.status), log.WARN)
        else:
            file_path = os.path.join(self.settings['APK_DOWNLOAD_DIR'], apk.apk_name)
            with open(file_path, 'wb') as f:
                f.write(response.body)
                apk.apk_package = file_path
                self.log('%s package download ok' % apk, log.INFO)
