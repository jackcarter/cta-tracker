from django.db import models
from django.utils import timezone

class Category(models.Model):
    title = models.CharField(max_length=100)

class Widget(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField()