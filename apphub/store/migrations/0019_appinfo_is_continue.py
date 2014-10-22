# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20141014_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='appinfo',
            name='is_continue',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u6301\u7eed\u6293\u53d6\u66f4\u65b0'),
            preserve_default=True,
        ),
    ]
