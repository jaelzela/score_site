# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0002_usercomment_userwebservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercomment',
            name='assigned_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='score_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userwebservice',
            name='assigned_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userwebservice',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userwebservice',
            name='score_date',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
