# -*- coding: utf-8 -*-
from scrapy.contrib.djangoitem import DjangoItem

from store.models import (
    Category, Tag, Permission, AppInfo
)


class CategoryItem(DjangoItem):
    django_model = Category


class TagItem(DjangoItem):
    django_model = Tag


class PermissionItem(DjangoItem):
    django_model = Permission


class AppItem(DjangoItem):
    django_model = AppInfo
