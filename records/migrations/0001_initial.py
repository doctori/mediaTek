# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(default='')),
            ],
            options={
                'ordering': ('id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(default='')),
                ('artist',models.ForeignKey(related_name='records', to='records.Artist')),
                ('ean', models.BigIntegerField(default=0, unique=True, verbose_name='EAN Code or any code that could identify the Item')),
                ('year',models.PositiveSmallIntegerField(default=2000)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('artist', 'name')]),
        ),
    ]
