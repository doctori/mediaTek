# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_auto_20150308_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='artist',
            field=models.ForeignKey(to='records.Artist'),
            preserve_default=True,
        ),
    ]
