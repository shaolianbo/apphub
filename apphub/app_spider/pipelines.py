# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy.exceptions import DropItem
from scrapy import log, Request
from scrapy.contrib.pipeline.images import ImagesPipeline

from store.models import AppIdentification, Permission, Category, Tag, Screenshot
from app_spider.items import AppIdentificationItem, AppInfoItem
from app_spider.signals import appinfo_saved


APK_DETAILS_FILED_NAMES = [
    'name', 'apk_name', 'last_version', 'rom', 'language', 'size', 'update_time', 'developer',
    'intro', 'download_url', 'score'
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
        name=item['category']
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
            origin_url=pic['url'],
        )
        shot.image = pic['path']
        shot.save()

    app.save()


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
            if 'top_type' in item and obj.top_type != item['top_type']:
                obj.top_type = item['top_type']
                obj.save()
            if created:
                log.msg('Get new apk %s' % obj.apk_name, level=log.INFO)
                return item
            else:
                raise DropItem('Duplicate apk %s' % obj.apk_name)

        if item.__class__ == AppInfoItem:
            app = item['instance']
            # 基本信息
            for key in APK_DETAILS_FILED_NAMES:
                setattr(app, key, item[key])
            app.logo = item['logo']['path']
            app.logo_origin_url = item['logo']['url']
            app.is_crawled = 1
            app.save()
            # 相关信息
            update_app_related(app, item)
            spider.log('update ok %s' % item['apk_name'], log.INFO)
            self.crawler.signals.send_catch_log(appinfo_saved, spider=spider, apk_name=app.apk_name)
            return item


class AppImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if 'logo' in item:
            yield Request(item['logo']['url'])
        if 'screenshots' in item:
            for shot in item['screenshots']:
                yield Request(shot['url'])

    def item_completed(self, results, item, info):
        """
        results 的数据结构:
        [(True, {url:'源地址', path:'存储地址'}), ... (False, Error)...]
        results 元素的顺序与get_media_requests中yield的顺序相同
        """
        if 'logo' in item:
            logo_result = results[0]
            if logo_result[0]:
                item['logo']['path'] = logo_result[1]['path']
            screenshots_results = results[1:]
        else:
            screenshots_results = results

        for i in range(len(item['screenshots'])):
            if screenshots_results[i][0]:
                item['screenshots'][i]['path'] = screenshots_results[i][1]['path']
        return item
