# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Email', models.CharField(max_length=40)),
                ('Title', models.CharField(max_length=100)),
                ('PageSerial', models.CharField(max_length=10)),
                ('SearchQuery', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['Title'],
                'verbose_name_plural': 'Visitors Bookmarks',
            },
        ),
        migrations.CreateModel(
            name='Zabayen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Email', models.CharField(max_length=40)),
                ('Pass', models.CharField(max_length=40)),
                ('Salt', models.CharField(max_length=40)),
            ],
            options={
                'ordering': ['Email'],
                'verbose_name_plural': 'Visitors Data',
            },
        ),
    ]
