# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20161028_2154'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SkillCategory',
            new_name='Skill_category',
        ),
    ]
