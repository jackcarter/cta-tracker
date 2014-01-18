from django.db import models
from django.utils import timezone


class Stop(models.Model):
    id = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.title
