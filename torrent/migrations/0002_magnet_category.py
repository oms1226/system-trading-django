# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torrent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='magnet',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
