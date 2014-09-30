# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy.exceptions import DropItem
from scrapy import log

from store.models import AppInfo, Permission, Category, Tag, Screenshot
from app_spider.items import ApkBaseItem, ApkDetailItem


APK_DES_MAP_MODEL_FIELD_NAME = {
    '软件名称': 'name',
    'APK名称': 'apk_name',
    '最新版本': 'last_version',
    '支持ROM': 'rom',
    '界面语言': 'language',
    '软件大小': 'size',
    '更新日期': 'update_time',
    '开发者': 'developer'
}


def update_app_related(app, item):
    """
    更新app关联数据
    """
    # permissions
    for name, desc in item['permissions']:
        permission, created = Permission.objects.get_or_create(
            name=name,
            desc=desc
        )
        app.permissions.add(permission)

    # category
    category, created = Category.objects.get_or_create(
        name=item['category']
    )
    app.category = category

    # tags
    for tag_name in item['tags']:
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
            category=category
        )
        app.add(tag)

    # screenshot
    # TODO: pic down load
    for url in item['image_urls'][1:]:
        Screenshot.objects.get_or_create(
            app=app,
            origin_url=url
        )

    app.save()


class StoreAppPipeline(object):
    def process_item(self, item, spider):
        spider.log('CNM pipeline', log.ERROR)
        if isinstance(item, ApkBaseItem):
            obj, created = AppInfo.objects.get_or_create(
                apk_name=item['apk_name'],
                name=item['name']
            )
            if created:
                log.msg('Get new apk %s' % obj.apk_name, level=log.INFO)
                yield item
            else:
                raise DropItem('Duplicate apk %s' % obj.apk_name)

        if isinstance(item, ApkDetailItem):
            try:
                app = AppInfo.objects.get(apk_name__exact=item['apk_name'])
            except AppInfo.DoesNotExist:
                raise DropItem('DoesNot exit %s in db' % item['apk_name'])
            # 基本信息
            app.score = float(item['score'])
            for key, val in item['details'].items():
                if key in APK_DES_MAP_MODEL_FIELD_NAME:
                    setattr(app, APK_DES_MAP_MODEL_FIELD_NAME[key], val)
                else:
                    log.msg('Unexpected detail key name %s' % key, level=log.WARNING)
            app.intro = item['intro']
            app.logo_origin_url = item['image_urls'][0]
            # TODO:download url
            app.is_crawled = 1
            app.save()

            update_app_related(app, item)
            yield item
