# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20141014_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appinfo',
            name='data_source',
            field=models.IntegerField(verbose_name='\u6570\u636e\u6765\u6e90', choices=[(1, '\u9177\u5b89'), (2, '\u8c4c\u8c46\u835a')]),
        ),
    ]
