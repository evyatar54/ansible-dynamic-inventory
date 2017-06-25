 # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    groups = models.ManyToManyField('self', blank=True)
    roles = models.ManyToManyField(Role, blank=True)
    isPlatform = models.BooleanField(default=False)
    enabled = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class Var(models.Model):
    group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return '{} : {}'.format(self.key, self.value)


class Host(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    groups = models.ManyToManyField(Group)
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.name





