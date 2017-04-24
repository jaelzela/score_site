# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0003_auto_20160211_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='ws_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
