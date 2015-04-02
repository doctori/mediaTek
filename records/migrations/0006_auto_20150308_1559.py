# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_auto_20150304_2049'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('artist', 'name')]),
        ),
    ]
