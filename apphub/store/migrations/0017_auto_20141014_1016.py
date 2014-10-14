# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20141014_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='appidentification',
            name='top_type',
            field=models.IntegerField(default=1, verbose_name='\u9876\u7ea7\u5206\u7c7b: \u5e94\u7528/\u6e38\u620f', choices=[(1, '\u5e94\u7528'), (2, '\u6e38\u620f')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appinfo',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='app\u540d\u79f0', blank=True),
        ),
    ]
