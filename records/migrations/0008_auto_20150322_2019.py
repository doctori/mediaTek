# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0007_auto_20150308_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='artist',
            field=models.ForeignKey(related_name='records', to='records.Artist'),
            preserve_default=True,
        ),
    ]
