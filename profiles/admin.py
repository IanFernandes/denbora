from django.contrib import admin

from profiles.models import City, SkillCategory, Skill, UserSkill

admin.site.register(City)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(UserSkill)

