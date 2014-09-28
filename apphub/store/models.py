# coding:utf8
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    """
    分类
    """
    name = models.CharField(max_length=50, verbose_name="app类型名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="app标签名称")
    category = models.ForeignKey(Category, verbose_name="所属分类")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="权限名称")
    desc = models.CharField(max_length=100, blank=True, null=True, verbose_name='权限描述')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "权限"


class AppInfo(models.Model):
    """
    app基本信息
    """
    apk_name = models.CharField(max_length=100, unique=True, verbose_name="apk包名称, app的唯一标识")
    name = models.CharField(max_length=255, verbose_name='app名称')
    categories = models.ForeignKey(Category, null=True, verbose_name="所属分类")
    tags = models.ManyToManyField(Tag, verbose_name="标签")
    score = models.IntegerField(default=0, verbose_name='评分')
    details = models.CharField(max_length=1024, blank=True, null=True, verbose_name='应用详情')
    permissions = models.ManyToManyField(Permission, verbose_name='权限')
    intro = models.CharField(max_length=1024, blank=True, null=True, verbose_name='应用简介')
    related_apps = models.ManyToManyField("self", verbose_name='相关应用')
    is_crawled = models.BooleanField(default=False, verbose_name='信息是否被抓取')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '应用基本信息'
