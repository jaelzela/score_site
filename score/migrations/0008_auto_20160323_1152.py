# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0007_userwebservice_info_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='ws',
            field=models.IntegerField(),
        ),
    ]
