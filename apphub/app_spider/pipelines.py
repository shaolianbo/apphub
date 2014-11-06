# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import json

from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.http import Request

from store.models import AppIdentification, Permission, Category, Tag, Screenshot, AppInfo
from app_spider.items import AppIdentificationItem, AppInfoItem
from app_spider.signals import crawl_success


APK_DETAILS_FILED_NAMES = [
    'name', 'apk_name', 'last_version', 'rom', 'language', 'size', 'developer',
    'intro', 'download_url', 'score', 'update_date', 'update_log', 'logo_origin_url'
]


def update_app_related(app, item):
    """
    更新app关联数据
    """
    # permissions
    for name, desc in item['permissions']:
        permission, created = Permission.objects.get_or_create(
            name=name
        )
        permission.desc = desc
        permission.save()
        app.permissions.add(permission)

    app.permissions_str = item['permissions_str']

    # category
    category, created = Category.objects.get_or_create(
        name=item['category'],
        top_type=app.app_id.top_type
    )

    # tags
    for tag_name in item['tags']:
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
        )
        category.tags.add(tag)
        app.tags.add(tag)

    app.category = category

    # screenshot
    for pic in item['screenshots']:
        shot, created = Screenshot.objects.get_or_create(
            app=app,
            origin_url=pic,
        )
        shot.save()

    app.save()


class FilterPipeline(object):
    """
    过滤不需要更新的app
    """
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        if self.crawler.settings['FORCE_UPDATE']:
            return item
        if item.__class__ == AppInfoItem:
            app = item['instance']
            if item['last_version'] and (item['last_version'] == app.last_version):
                self.crawler.signals.send_catch_log(crawl_success, spider=spider, apk_name=app.app_id.apk_name, reason='版本已最新,不需要更新')
                raise DropItem('%s(%s) version is newest' % (app.app_id.apk_name, app.last_version))
            else:
                return item
        else:
            return item


class StoreAppPipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        if item.__class__ == AppIdentificationItem:
            obj, created = AppIdentification.objects.get_or_create(
                apk_name=item['apk_name']
            )
            if 'top_type' in item and (item['top_type'] != obj.top_type):
                obj.top_type = item['top_type']
                obj.save()
            if 'category' in item:
                cat, is_created = Category.objects.get_or_create(name=item['category'], top_type=item['top_type'])
            if created:
                appinfo = AppInfo(app_id=obj, data_source=item['data_source'])
                appinfo.save()
                log.msg('Get new apk %s' % obj.apk_name, level=log.INFO)
                return item
            else:
                raise DropItem('Duplicate apk %s' % obj.apk_name)

        if item.__class__ == AppInfoItem:
            app = item['instance']
            # 基本信息
            for key in APK_DETAILS_FILED_NAMES:
                setattr(app, key, item[key])
            app.is_crawled = 1
            app.last_crawl_time = datetime.now()
            app.save()
            # 相关信息
            update_app_related(app, item)
            spider.log('update ok %s' % item['apk_name'], log.INFO)
            # sync data to Doraemon
            url = "%s/?apk_name=%s" % (self.crawler.settings['DATA_SYNC_API'], app.app_id.apk_name)
            if self.crawler.settings.get('IS_INSERT_DORAEMON', False):
                url += '&insert=1'

            # 返回defer, 同步到Doraemon
            request = Request(url=url)
            request.callback = None
            request.errback = None
            dfd = self.crawler.engine.download(request, spider)
            dfd.addCallbacks(
                callback=self._sync_callback, callbackArgs=(item['apk_name'], spider),
                errback=self._sync_errback, errbackArgs=(item['apk_name'], spider))
            dfd.addErrback(spider.log, level=log.ERROR)
            return dfd.addBoth(lambda _: item)

    def _sync_callback(self, response, apk_name, spider):
        if response.status != 200:
            spider.log('同步%s失败: %s' % (apk_name, response.status), log.INFO)
            return
        body = json.loads(response.body)
        if body['success']:
            self.crawler.signals.send_catch_log(crawl_success, spider=spider, apk_name=apk_name, reason='抓取成功')
            spider.log('同步%s成功' % apk_name, log.INFO)
        else:
            spider.log('同步%s失败: %s' % (apk_name, response.body), log.ERROR)

    def _sync_errback(self, failure, apk_name, spider):
        spider.log('API访问异常%s: %s' % (apk_name, failure.value), log.ERROR)
