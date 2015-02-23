# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='artist',
            name='name',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
