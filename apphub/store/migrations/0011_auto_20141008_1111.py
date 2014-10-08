# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20140929_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='category',
        ),
        migrations.AddField(
            model_name='tag',
            name='categories',
            field=models.ManyToManyField(to='store.Category', verbose_name='\u6240\u5c5e\u5206\u7c7b'),
            preserve_default=True,
        ),
    ]
