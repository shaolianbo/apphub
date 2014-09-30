# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20140929_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appinfo',
            name='score',
            field=models.FloatField(default=0, verbose_name='\u8bc4\u5206'),
        ),
    ]
