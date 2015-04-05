# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20150405_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='ean',
            field=models.BigIntegerField(unique=True, verbose_name='EAN Code or any code that could identify the Item'),
            preserve_default=True,
        ),
    ]
