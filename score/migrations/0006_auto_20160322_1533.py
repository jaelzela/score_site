# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-22 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0005_userwebservice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='webservice',
            name='articles',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='webservice',
            name='developers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='webservice',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='webservice',
            name='mashups',
            field=models.IntegerField(default=0),
        ),
    ]
