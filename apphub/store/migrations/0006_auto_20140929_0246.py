# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20140929_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='appinfo',
            name='download_url',
            field=models.URLField(null=True, verbose_name='\u4e0b\u8f7d\u5730\u5740', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='logo',
            field=models.ImageField(upload_to='logo', null=True, verbose_name='app\u56fe\u6807', blank=True),
            preserve_default=True,
        ),
    ]
