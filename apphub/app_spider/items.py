# -*- coding: utf-8 -*-
from scrapy.item import Field, Item
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Identity, Join

from store.models import AppInfo


class ItemInvalidException(Exception):
    item_field_msg = 'exception'

    def __init__(self, item, field_names):
        self.field_names = field_names or []
        if type(self.field_names) != list:
            self.field_names = [self.field_names]
        self.item_class = item.__class__.__name__ or ''
        self.msg = 'exception'

    def __str__(self):
        field_str = '(' + ','.join(self.field_names) + ')'
        return "ItemInvalid %s %s : %s" % (self.item_class, field_str, self.item_field_msg)


class LackForFieldError(ItemInvalidException):
    item_field_msg = 'field should be assigned a value'


class EmptyCrawlResultExcption(ItemInvalidException):
    item_field_msg = 'fied get empty value from web'


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

    def is_valid(self):
        for name, field in self.fields.items():
            if name not in self._values:
                if 'default' not in field:
                    raise LackForFieldError(self, name)
        return True


class AppInfoItem(DefaultsItem):
    instance = Field()
    apk_name = Field()
    category = Field()
    name = Field(default='')
    score = Field(default=0)
    details = Field(default={})
    permissions = Field(default=[])
    permissions_str = Field(default="")
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
    default_item_class = AppInfoItem

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
