# -*- coding: utf-8 -*-
from scrapy.item import Field, Item, ItemMeta


class SimpleItemMeta(ItemMeta):
    def __new__(cls, class_name, bases, attrs):
        newcls = super(SimpleItemMeta, cls).__new__(cls, class_name, bases, attrs)
        newcls.fields = newcls.fields.copy()
        if newcls.custom_field_name:
            for key in newcls.custom_field_name:
                if key not in newcls.fields:
                    newcls.fields[key] = Field()
        return newcls


class AppIdentificationItem(Item):
    """
    app列表页中抓取, apk_name
    """
    apk_name = Field()
    top_type = Field()


class AppInfoItem(Item):
    """
    app详情页item:
    image_urls: 第一个url是logo, 之后的url为app截屏
    """
    __metaclass__ = SimpleItemMeta
    custom_field_name = [
        'apk_name', 'name', 'score', 'details', 'permissions', 'category', 'tags', 'intro',
        'download_url', 'logo', 'screenshots', 'instance', 'data_source', 'permissions_str'
    ]
