# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 19:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20161028_2155'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skill_category',
            new_name='SkillCategory',
        ),
    ]
