from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from profiles.models import City


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, default=None)
    denboras = models.SmallIntegerField(default=0)
    city = models.ForeignKey(City, default=1)
    description = models.TextField(default="", null=True)

    def __str__(self):
        return self.username