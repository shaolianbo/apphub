# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20141008_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appinfo',
            name='last_version',
            field=models.CharField(max_length=100, null=True, verbose_name='\u6700\u65b0\u7248\u672c', blank=True),
        ),
        migrations.AlterField(
            model_name='appinfo',
            name='rom',
            field=models.CharField(max_length=100, null=True, verbose_name='\u652f\u6301ROM', blank=True),
        ),
    ]
