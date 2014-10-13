# coding:utf8
from __future__ import unicode_literals

from django.db import models


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="app标签名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Category(models.Model):
    """
    分类
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="app类型名称")
    tags = models.ManyToManyField(Tag, verbose_name='标签')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'


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


class AppIdentification(models.Model):
    """
    app 唯一标识: 抓取数据的基础
    """
    apk_name = models.CharField(max_length=100, unique=True, verbose_name="apk包名称, app的唯一标识")

    def __unicode__(self):
        return self.apk_name

    class Meta:
        verbose_name = verbose_name_plural = 'app唯一标识'


class AppInfo(models.Model):
    """
    app信息
    """
    COOLAPK = 1
    WANDOUJIA = 2
    DATA_SOURCE_CHOICES = (
        ('1', '酷安'),
        ('2', '豌豆荚')
    )
    app_id = models.ForeignKey(AppIdentification, verbose_name='应用唯一标识')
    data_source = models.IntegerField(choices=DATA_SOURCE_CHOICES, verbose_name='数据来源')
    name = models.CharField(max_length=255, verbose_name='app名称')
    logo = models.ImageField(upload_to='logo', blank=True, null=True, verbose_name='app图标')
    logo_origin_url = models.URLField(max_length=200, blank=True, null=True, verbose_name='coolapk logo下载地址')
    download_url = models.URLField(max_length=200, blank=True, null=True, verbose_name='下载地址')
    apk_package = models.FileField(upload_to='apks', blank=True, null=True, verbose_name='apk包的本地存储地址')
    category = models.ForeignKey(Category, null=True, verbose_name="所属分类")
    tags = models.ManyToManyField(Tag, verbose_name="标签")
    score = models.FloatField(default=0, verbose_name='评分')
    permissions = models.ManyToManyField(Permission, verbose_name='权限')
    permissions_str = models.CharField(max_length=1024, blank=True, null=True, verbose_name="权限字符串", help_text="如果爬虫只能爬到权限的中文名称,就存储这些字符串")
    intro = models.CharField(max_length=10240, blank=True, null=True, verbose_name='应用简介')
    is_crawled = models.BooleanField(default=False, verbose_name='信息是否被抓取')
    # 应用详情
    last_version = models.CharField(max_length=100, blank=True, null=True, verbose_name='最新版本')
    rom = models.CharField(max_length=100, blank=True, null=True, verbose_name='支持ROM')
    language = models.CharField(max_length=20, blank=True, null=True, verbose_name='界面语言')
    size = models.CharField(max_length=20, blank=True, null=True, verbose_name='软件大小')
    update_time = models.CharField(max_length=20, blank=True, null=True, verbose_name='更新日期')
    developer = models.CharField(max_length=50, blank=True, null=True, verbose_name='开发者')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '应用信息'
        unique_together = ('app_id', 'data_source')


class Screenshot(models.Model):
    app = models.ForeignKey(AppInfo, verbose_name="所属应用")
    image = models.ImageField(upload_to="screenshot", verbose_name="截图")
    origin_url = models.URLField(max_length=200, blank=True, null=True, verbose_name='coolapk 截图下载地址')

    def __unicode__(self):
        return "%s_截图:%s" % (self.app.name, self.id)

    class Meta:
        verbose_name = verbose_name_plural = "截图"
