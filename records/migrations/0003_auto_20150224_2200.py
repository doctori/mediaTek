# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_auto_20150223_2055'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='record',
            name='artist',
        ),
    ]
