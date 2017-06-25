 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class Var(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return '{} : {}'.format(self.key, self.value)


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    groups = models.ManyToManyField('self')
    roles = models.ManyToManyField(Role, blank=True)
    isPlatform = models.BooleanField()
    enabled = models.BooleanField(default=False)
    variables = models.OneToManyField(Var)

    def __str__(self):
        return self.name

class Host(models.Model):
    name = models.CharField(max_length=255, unique=True)
    groups = models.ManyToManyField(Group)
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.name





