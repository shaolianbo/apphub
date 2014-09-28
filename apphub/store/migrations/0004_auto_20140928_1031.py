# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20140928_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apk_name', models.CharField(unique=True, max_length=100, verbose_name='apk\u5305\u540d\u79f0, app\u7684\u552f\u4e00\u6807\u8bc6')),
                ('name', models.CharField(max_length=255, verbose_name='app\u540d\u79f0')),
                ('score', models.IntegerField(default=0, verbose_name='\u8bc4\u5206')),
                ('details', models.CharField(max_length=1024, null=True, verbose_name='\u5e94\u7528\u8be6\u60c5', blank=True)),
                ('intro', models.CharField(max_length=1024, null=True, verbose_name='\u5e94\u7528\u7b80\u4ecb', blank=True)),
                ('is_crawled', models.BooleanField(default=False, verbose_name='\u4fe1\u606f\u662f\u5426\u88ab\u6293\u53d6')),
                ('categories', models.ForeignKey(verbose_name='\u6240\u5c5e\u5206\u7c7b', to='store.Category', null=True)),
                ('permissions', models.ManyToManyField(to='store.Permission', verbose_name='\u6743\u9650')),
                ('related_apps', models.ManyToManyField(related_name='related_apps_rel_+', verbose_name='\u76f8\u5173\u5e94\u7528', to='store.AppInfo')),
                ('tags', models.ManyToManyField(to='store.Tag', verbose_name='\u6807\u7b7e')),
            ],
            options={
                'verbose_name': '\u5e94\u7528\u57fa\u672c\u4fe1\u606f',
                'verbose_name_plural': '\u5e94\u7528\u57fa\u672c\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='app',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='app',
            name='permissions',
        ),
        migrations.RemoveField(
            model_name='app',
            name='related_apps',
        ),
        migrations.RemoveField(
            model_name='app',
            name='tags',
        ),
        migrations.DeleteModel(
            name='App',
        ),
    ]
