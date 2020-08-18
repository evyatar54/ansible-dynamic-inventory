 # -*- coding: utf-8 -*-
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    children = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='parents')
    roles = models.ManyToManyField(Role, blank=True)
    isPlatform = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Var(models.Model):
    group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE, related_name='vars')
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ("group", "key")

    def __str__(self):
        return '{} : {}'.format(self.key, self.value)


class Host(models.Model):
    name = models.CharField(max_length=255, unique=True)
    groups = models.ManyToManyField(Group, related_name="hosts")
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.name
