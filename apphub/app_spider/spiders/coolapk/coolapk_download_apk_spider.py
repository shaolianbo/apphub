# coding:utf8
import os

import scrapy
from scrapy.http import Request
from scrapy import log

from store.models import AppInfo


class CoolApkDownloadApkSpider(scrapy.Spider):
    name = 'coolapk_package'
    allowed_domains = ['coolapk.com']

    def __init__(self, apk_name=None, *args, **kwargs):
        self.apk_name = apk_name

    def start_requests(self):
        """
        首先访问主站,获得cookie, 所以 COOKIES_ENABLED = True
        """
        yield Request('http://coolapk.com'+'/apk/'+self.apk_name, callback=self.start_download)

    def start_download(self, response):
        self.SESSID = None
        for cookie in response.headers['Set-Cookie']:
            for cookie_attr in cookie.split(';'):
                cookie_key_vale = cookie_attr.split('=')
                if 'SESSID' == cookie_key_vale[0]:
                    self.SESSID = cookie_key_vale[1]
                    break
            if self.SESSID:
                break
        if self.apk_name:
            try:
                apk = AppInfo.objects.get(apk_name__exact=self.apk_name)
            except AppInfo.DoesNotExist:
                self.log("%s does not exits in db" % self.apk_name, log.ERROR)
                return
            if apk.download_url:
                download_url = apk.download_url.startswith('http') and apk.download_url or 'http://'+apk.download_url
                req = Request(download_url, callback=self.complete_download, cookies={'SESSID': self.SESSID})
                req.meta['apk_instance'] = apk
                yield req
            else:
                return
        else:
            apks_without_package = AppInfo.objects.filter(apk_package__isnull=True, is_crawled__exact=1, download_url__isnull=False)
            for apk in apks_without_package:
                download_url = apk.download_url.startswith('http') and apk.download_url or 'http://'+apk.download_url
                req = Request(download_url, callback=self.complete_download)
                req.meta['apk_instance'] = apk
                yield req

    def complete_download(self, response):
        apk_instance = response.meta['apk_instance']
        if response.status != 200:
            self.log("%s package download failed: %s" % (apk_instance, response.status), log.WARN)
        else:
            file_path = os.path.join(self.settings['APK_DOWNLOAD_DIR'], apk_instance.apk_name)
            with open(file_path, 'wb') as f:
                f.write(response.body)
                apk_instance.apk_package = file_path
                apk_instance.save()
                self.log('%s package download ok' % apk_instance, log.INFO)
