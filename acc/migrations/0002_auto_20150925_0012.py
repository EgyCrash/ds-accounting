# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='created_at',
            field=models.TimeField(auto_now=True),
        ),
    ]
