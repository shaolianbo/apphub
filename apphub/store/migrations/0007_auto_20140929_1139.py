# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20140929_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='appinfo',
            name='logo_origin_url',
            field=models.URLField(null=True, verbose_name='coolapk logo\u4e0b\u8f7d\u5730\u5740', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='screenshot',
            name='origin_url',
            field=models.URLField(null=True, verbose_name='coolapk \u622a\u56fe\u4e0b\u8f7d\u5730\u5740', blank=True),
            preserve_default=True,
        ),
    ]
