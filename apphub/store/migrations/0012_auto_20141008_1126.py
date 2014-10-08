# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20141008_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='categories',
        ),
        migrations.AddField(
            model_name='category',
            name='tags',
            field=models.ManyToManyField(to='store.Tag', verbose_name='\u6807\u7b7e'),
            preserve_default=True,
        ),
    ]
