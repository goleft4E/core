# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-16 10:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0003_add_more_sources'),
    ]

    operations = [
        migrations.AddField(
            model_name='annmodel',
            name='new_timestamp',
            field=models.DateTimeField(null=True),
        ),
    ]
