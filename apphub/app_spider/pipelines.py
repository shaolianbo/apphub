# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from scrapy.exceptions import DropItem
from scrapy import log, Request
from scrapy.contrib.pipeline.images import ImagesPipeline

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
            name=name
        )
        permission.desc = desc
        permission.save()
        app.permissions.add(permission)

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
            image=pic['path']       # 这里没有在upload_to的子目录下
        )
        shot.image = pic['path']
        shot.save()

    app.save()


class StoreAppPipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == ApkBaseItem:
            obj, created = AppInfo.objects.get_or_create(
                apk_name=item['apk_name']
            )
            obj.name = item['name']
            obj.save()
            if created:
                log.msg('Get new apk %s' % obj.apk_name, level=log.INFO)
                return item
            else:
                raise DropItem('Duplicate apk %s' % obj.apk_name)

        if item.__class__ == ApkDetailItem:
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
            app.logo = item['logo']['path']
            app.logo_origin_url = item['logo']['url']
            app.is_crawled = 1
            app.save()
            update_app_related(app, item)
            spider.log('update ok %s' % item['apk_name'], log.INFO)
            return item


class AppImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['logo'])
        for url in item['screenshots']:
            yield Request(url)

    def item_completed(self, results, item, info):
        logo_result = results[0]
        if logo_result[0]:
            item['logo'] = {
                'path': logo_result[1]['path'],
                'url':  logo_result[1]['url']
            }
        else:
            item['logo'] = {
                'path': "",
                'url': item['logo']
            }

        screenshots_results = results[1:]
        screenshots = []
        for i in range(len(item['screenshots'])):
            pic = {'url': item['screenshots'][i], 'path': ''}
            if screenshots_results[i][0]:
                pic['path'] = screenshots_results[i][1]['path']
            screenshots.append(pic)
        item['screenshots'] = screenshots
        return item
