from __future__ import unicode_literals

from django.db import models
from denbora_project.settings import AUTH_USER_MODEL


class Message(models.Model):
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name="sender")
    receiver = models.ForeignKey(AUTH_USER_MODEL, related_name="receiver")
    title = models.CharField(max_length=100, null=True)
    msg_content = models.TextField(null=False)
    created_at = models.DateTimeField()
    read = models.BooleanField(default=False)  # When receiver reads the message

    def __str__(self):
        return self.msg_content