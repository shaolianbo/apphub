# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20140929_1139'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appinfo',
            old_name='categories',
            new_name='category',
        ),
    ]
