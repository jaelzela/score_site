from __future__ import unicode_literals

from django.db import models

class MaxMin(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    mean = models.FloatField(default=0.0)
    stdev = models.FloatField(default=0.0)