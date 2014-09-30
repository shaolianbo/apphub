# coding:utf8
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    """
    分类
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="app类型名称")

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
    app信息
    """
    apk_name = models.CharField(max_length=100, unique=True, verbose_name="apk包名称, app的唯一标识")
    name = models.CharField(max_length=255, verbose_name='app名称')
    logo = models.ImageField(upload_to='logo', blank=True, null=True, verbose_name='app图标')
    logo_origin_url = models.URLField(max_length=200, blank=True, null=True, verbose_name='coolapk logo下载地址')
    download_url = models.URLField(max_length=200, blank=True, null=True, verbose_name='下载地址')
    category = models.ForeignKey(Category, null=True, verbose_name="所属分类")
    tags = models.ManyToManyField(Tag, verbose_name="标签")
    score = models.FloatField(default=0, verbose_name='评分')
    permissions = models.ManyToManyField(Permission, verbose_name='权限')
    intro = models.CharField(max_length=1024, blank=True, null=True, verbose_name='应用简介')
    is_crawled = models.BooleanField(default=False, verbose_name='信息是否被抓取')
    # 应用详情
    last_version = models.CharField(max_length=20, blank=True, null=True, verbose_name='最新版本')
    rom = models.CharField(max_length=50, blank=True, null=True, verbose_name='支持ROM')
    language = models.CharField(max_length=20, blank=True, null=True, verbose_name='界面语言')
    size = models.CharField(max_length=20, blank=True, null=True, verbose_name='软件大小')
    update_time = models.CharField(max_length=20, blank=True, null=True, verbose_name='更新日期')
    developer = models.CharField(max_length=50, blank=True, null=True, verbose_name='开发者')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '应用信息'


class Screenshot(models.Model):
    app = models.ForeignKey(AppInfo, verbose_name="所属应用")
    image = models.ImageField(upload_to="screenshot", verbose_name="截图")
    origin_url = models.URLField(max_length=200, blank=True, null=True, verbose_name='coolapk 截图下载地址')

    def __unicode__(self):
        return "%s_截图:%s" % (self.app.name, self.id)

    class Meta:
        verbose_name = verbose_name_plural = "截图"
