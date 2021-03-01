import uuid

from django.db import models
from django.contrib.sessions.models import Session


# Create your models here.

class AnonymousUser(models.Model):
    id = models.IntegerField(primary_key=True)
    session = models.ForeignKey('sessions.Session',
                                on_delete=models.SET_NULL,
                                null=True)
