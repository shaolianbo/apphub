# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_app_is_crawled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='categories',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u5206\u7c7b', to='store.Category', null=True),
        ),
    ]
