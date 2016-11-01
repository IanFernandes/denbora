from __future__ import unicode_literals
from django.db import models
from denbora_project.settings import AUTH_USER_MODEL


class City(models.Model):
    name = models.TextField(null=False)
    complete_location = models.TextField(null=False)
    country_code = models.CharField(max_length=2, null=True)
    lat = models.FloatField(null=False)
    lon = models.FloatField(null=False)

    def __str__(self):
        return self.complete_location.encode('UTF-8')


class SkillCategory(models.Model):
    name = models.CharField(max_length=50, null=False, default='Unknown')

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(SkillCategory)
    desc = models.TextField(null=False)

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    skill = models.ForeignKey(Skill)

    def __str__(self):
        return str(self.id) + ' | ' + self.user.username + ' | ' + self.skill.name
