# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0002_auto_20150421_0959'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmark',
            old_name='ID',
            new_name='bookmark_id',
        ),
    ]
