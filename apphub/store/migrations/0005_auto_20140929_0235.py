# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20140928_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to='screenshot', verbose_name='\u622a\u56fe')),
                ('app', models.ForeignKey(verbose_name='\u6240\u5c5e\u5e94\u7528', to='store.AppInfo')),
            ],
            options={
                'verbose_name': '\u622a\u56fe',
                'verbose_name_plural': '\u622a\u56fe',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='appinfo',
            options={'verbose_name': '\u5e94\u7528\u4fe1\u606f', 'verbose_name_plural': '\u5e94\u7528\u4fe1\u606f'},
        ),
        migrations.RemoveField(
            model_name='appinfo',
            name='details',
        ),
        migrations.RemoveField(
            model_name='appinfo',
            name='related_apps',
        ),
        migrations.AddField(
            model_name='appinfo',
            name='developer',
            field=models.CharField(max_length=50, null=True, verbose_name='\u5f00\u53d1\u8005', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='language',
            field=models.CharField(max_length=20, null=True, verbose_name='\u754c\u9762\u8bed\u8a00', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='last_version',
            field=models.CharField(max_length=20, null=True, verbose_name='\u6700\u65b0\u7248\u672c', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='rom',
            field=models.CharField(max_length=50, null=True, verbose_name='\u652f\u6301ROM', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='size',
            field=models.CharField(max_length=20, null=True, verbose_name='\u8f6f\u4ef6\u5927\u5c0f', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='update_time',
            field=models.CharField(max_length=20, null=True, verbose_name='\u66f4\u65b0\u65e5\u671f', blank=True),
            preserve_default=True,
        ),
    ]
