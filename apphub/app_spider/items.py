# -*- coding: utf-8 -*-
from scrapy.item import Field, Item, ItemMeta
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity, Join

from store.models import AppInfo


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


class DefaultsItem(Item):
    """ Item with default values """
    def __getitem__(self, key):
        try:
            return self._values[key]
        except KeyError:
            field = self.fields[key]
            if 'default' in field:
                return field['default']
            raise


class AppInfoItem(DefaultsItem):
    instance = Field()
    apk_name = Field()
    name = Field(default='')
    score = Field(default=0)
    details = Field(default={})
    permissions = Field(default=[])
    permissions_str = Field(default="")
    category = Field()
    tags = Field(default=[])
    intro = Field(default='')
    download_url = Field(default='')
    logo = Field(default='')
    screenshots = Field(default=[])
    data_source = Field(default=AppInfo.WANDOUJIA)
    last_version = Field(default='')
    rom = Field(default='')
    language = Field(default='')
    size = Field(default='')
    update_time = Field(default=None)
    developer = Field(default='')


def image_field_in_processor(url):
    return {'url': url, 'path': ''}


class AppInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(unicode.strip)

    logo_in = MapCompose(image_field_in_processor)

    screenshots_in = MapCompose(image_field_in_processor)
    screenshots_out = Identity()

    intro_out = Join('<br>')

    tags_out = Identity()

    permissions_str_out = Join(';')

    permissions_out = Identity()

    instance_in = Identity()
