# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_appinfo_is_continue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appinfo',
            name='update_time',
        ),
        migrations.AddField(
            model_name='appinfo',
            name='last_crawl_time',
            field=models.DateTimeField(null=True, verbose_name='\u6700\u540e\u6293\u53d6\u65f6\u95f4', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='update_date',
            field=models.DateField(null=True, verbose_name='\u66f4\u65b0\u65e5\u671f', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='update_log',
            field=models.TextField(null=True, verbose_name='\u66f4\u65b0\u8bb0\u5f55', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appinfo',
            name='intro',
            field=models.TextField(null=True, verbose_name='\u5e94\u7528\u7b80\u4ecb', blank=True),
        ),
    ]
