# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20141022_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='top_type',
            field=models.IntegerField(default=1, verbose_name='\u9876\u7ea7\u5206\u7c7b: \u5e94\u7528/\u6e38\u620f', choices=[(1, '\u5e94\u7528'), (2, '\u6e38\u620f')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='app\u7c7b\u578b\u540d\u79f0'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('name', 'top_type')]),
        ),
    ]
