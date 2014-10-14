# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20141008_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='appinfo',
            name='apk_package',
            field=models.FileField(upload_to='apks', null=True, verbose_name='apk\u5305\u7684\u672c\u5730\u5b58\u50a8\u5730\u5740', blank=True),
            preserve_default=True,
        ),
    ]
