# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_auto_20150224_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='artist',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='ean',
            field=models.BigIntegerField(default=0, unique=True, verbose_name='EAN Code or any code that could identify the Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='record',
            name='year',
            field=models.PositiveSmallIntegerField(default=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='artist',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='record',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
