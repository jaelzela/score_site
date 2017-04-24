# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_username', models.CharField(max_length=30)),
                ('cmt_id', models.IntegerField()),
                ('score', models.IntegerField()),
                ('assigned_date', models.DateTimeField()),
                ('score_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWebService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_username', models.CharField(max_length=30)),
                ('ws_id', models.IntegerField()),
                ('score', models.IntegerField()),
                ('assigned_date', models.DateTimeField()),
                ('score_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
