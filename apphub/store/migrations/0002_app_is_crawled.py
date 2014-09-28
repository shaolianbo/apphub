# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='is_crawled',
            field=models.BooleanField(default=False, verbose_name='\u4fe1\u606f\u662f\u5426\u88ab\u6293\u53d6'),
            preserve_default=True,
        ),
    ]
