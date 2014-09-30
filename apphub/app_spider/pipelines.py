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
        app.tags.add(tag)

    # screenshot
    index = 1
    for is_downloaded, info in item['images'][1:]:
        if is_downloaded:
            Screenshot.objects.get_or_create(
                app=app,
                origin_url=info['url'],
                image=info['path']       # 这里没有在upload_to的子目录下
            )
        else:
            Screenshot.objects.get_or_create(
                app=app,
                origin_url=item['image_urls'][index],
                image=None
            )
        index += 1
    app.save()


class StoreAppPipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == ApkBaseItem:
            obj, created = AppInfo.objects.get_or_create(
                apk_name=item['apk_name'],
                name=item['name']
            )
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
            # image_urls 与 images 对应; images 是 image_urls下载后的结果
            # image_urls[0] 是 logo  ; image_urls[1:] 是截屏
            # image_urls 是 url列表 [ url1, url2 ...]
            # images 结构:[{'path': <存储路径> , 'url': <url> }), ... ]
            if len(item['image_urls']):
                app.logo_origin_url = item['image_urls'][0]
                if item['images'][0][0]:
                    app.logo = item['images'][0][1]['path']
            app.logo = item['im']
            # TODO:download url
            app.is_crawled = 1
            app.save()

            update_app_related(app, item)
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

        screenshots_results = results[1:0]
        screenshots = []
        for i in range(len(item['screenshots'])):
            pic = {'url': item['screenshots'][i], }
            if screenshots_results[i][0]:
                
                
        image_paths = [x['path'] for ok, x in results if ok]
        item['image_paths'] = image_paths
        return item
