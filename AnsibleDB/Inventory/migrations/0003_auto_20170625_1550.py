# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0002_auto_20170625_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='variables',
        ),
        migrations.AddField(
            model_name='var',
            name='group',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Inventory.Group'),
            preserve_default=False,
        ),
    ]
