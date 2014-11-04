# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20141023_0829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appinfo',
            name='apk_package',
        ),
        migrations.RemoveField(
            model_name='appinfo',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='screenshot',
            name='image',
        ),
    ]
