# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_appinfo_apk_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppIdentification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apk_name', models.CharField(unique=True, max_length=100, verbose_name='apk\u5305\u540d\u79f0, app\u7684\u552f\u4e00\u6807\u8bc6')),
            ],
            options={
                'verbose_name': 'app\u552f\u4e00\u6807\u8bc6',
                'verbose_name_plural': 'app\u552f\u4e00\u6807\u8bc6',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='appinfo',
            name='apk_name',
        ),
        migrations.AddField(
            model_name='appinfo',
            name='app_id',
            field=models.ForeignKey(default=1, verbose_name='\u5e94\u7528\u552f\u4e00\u6807\u8bc6', to='store.AppIdentification'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='data_source',
            field=models.IntegerField(default=1, verbose_name='\u6570\u636e\u6765\u6e90', choices=[('1', '\u9177\u5b89'), ('2', '\u8c4c\u8c46\u835a')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appinfo',
            name='permissions_str',
            field=models.CharField(help_text='\u5982\u679c\u722c\u866b\u53ea\u80fd\u722c\u5230\u6743\u9650\u7684\u4e2d\u6587\u540d\u79f0,\u5c31\u5b58\u50a8\u8fd9\u4e9b\u5b57\u7b26\u4e32', max_length=1024, null=True, verbose_name='\u6743\u9650\u5b57\u7b26\u4e32', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='appinfo',
            unique_together=set([('app_id', 'data_source')]),
        ),
    ]
