 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from datetime import datetime


class Role(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    groups = models.ManyToManyField('self', symmetrical=False, blank=True)
    roles = models.ManyToManyField(Role, blank=True)
    isPlatform = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.get_string())
        # return self.name

    def get_string(self):
        if self.groups.count() == 0:
            string_builder = ''
        else:
            string_builder = 'in groups:\n  '
            for g in self.groups.all():
                string_builder += str(g.name) + ', '
        return string_builder


# class Var(models.Model):
#     group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE)
#     key = models.CharField(max_length=255)
#     value = models.CharField(max_length=255)
#
#     class Meta:
#         unique_together = ("group", "key")
#
#     def __str__(self):
#         return '{} : {}, group: {}'.format(self.key, self.value+'-sudoers')


class Host(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    groups = models.ManyToManyField(Group)
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.name