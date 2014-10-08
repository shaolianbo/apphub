# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20141008_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appinfo',
            name='intro',
            field=models.CharField(max_length=10240, null=True, verbose_name='\u5e94\u7528\u7b80\u4ecb', blank=True),
        ),
    ]
