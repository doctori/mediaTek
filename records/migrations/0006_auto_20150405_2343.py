# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_auto_20150405_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='year',
            field=models.PositiveSmallIntegerField(default=2000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
