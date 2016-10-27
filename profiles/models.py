from __future__ import unicode_literals
from django.db import models


class City(models.Model):
    name = models.TextField(null=False)
    complete_location = models.TextField(null=False)
    country_code = models.CharField(max_length=2, null=True)
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)
