# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apk_name', models.CharField(unique=True, max_length=100, verbose_name='apk\u5305\u540d\u79f0, app\u7684\u552f\u4e00\u6807\u8bc6')),
                ('name', models.CharField(max_length=255, verbose_name='app\u540d\u79f0')),
                ('score', models.IntegerField(default=0, verbose_name='\u8bc4\u5206')),
                ('details', models.CharField(max_length=1024, null=True, verbose_name='\u5e94\u7528\u8be6\u60c5', blank=True)),
                ('intro', models.CharField(max_length=1024, null=True, verbose_name='\u5e94\u7528\u7b80\u4ecb', blank=True)),
            ],
            options={
                'verbose_name': '\u5e94\u7528\u57fa\u672c\u4fe1\u606f',
                'verbose_name_plural': '\u5e94\u7528\u57fa\u672c\u4fe1\u606f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='app\u7c7b\u578b\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u6743\u9650\u540d\u79f0')),
                ('desc', models.CharField(max_length=100, null=True, verbose_name='\u6743\u9650\u63cf\u8ff0', blank=True)),
            ],
            options={
                'verbose_name': '\u6743\u9650',
                'verbose_name_plural': '\u6743\u9650',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='app\u6807\u7b7e\u540d\u79f0')),
                ('category', models.ForeignKey(verbose_name='\u6240\u5c5e\u5206\u7c7b', to='store.Category')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='app',
            name='categories',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u5206\u7c7b', to='store.Category'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='permissions',
            field=models.ManyToManyField(to='store.Permission', verbose_name='\u6743\u9650'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='related_apps',
            field=models.ManyToManyField(related_name='related_apps_rel_+', verbose_name='\u76f8\u5173\u5e94\u7528', to='store.App'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='app',
            name='tags',
            field=models.ManyToManyField(to='store.Tag', verbose_name='\u6807\u7b7e'),
            preserve_default=True,
        ),
    ]
