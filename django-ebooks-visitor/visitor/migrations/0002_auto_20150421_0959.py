# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='id',
        ),
        migrations.AddField(
            model_name='bookmark',
            name='ID',
            field=models.CharField(default=1, max_length=100, serialize=False, primary_key=True),
            preserve_default=False,
        ),
    ]
