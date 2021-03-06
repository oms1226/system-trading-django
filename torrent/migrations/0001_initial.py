# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-21 06:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Magnet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(db_index=True, max_length=255)),
                ('category', models.CharField(db_index=True, max_length=50)),
                ('title', models.TextField()),
                ('magnet', models.CharField(db_index=True, max_length=100)),
                ('reg_date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
    ]
