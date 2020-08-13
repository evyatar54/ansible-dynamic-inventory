# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-08-13 20:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('isPlatform', models.BooleanField(default=False)),
                ('enabled', models.BooleanField(default=True)),
                ('children', models.ManyToManyField(blank=True, related_name='parents', to='Inventory.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('groups', models.ManyToManyField(to='Inventory.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Var',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vars', to='Inventory.Group')),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='roles',
            field=models.ManyToManyField(blank=True, to='Inventory.Role'),
        ),
        migrations.AddField(
            model_name='group',
            name='roles',
            field=models.ManyToManyField(blank=True, to='Inventory.Role'),
        ),
        migrations.AlterUniqueTogether(
            name='var',
            unique_together=set([('group', 'key')]),
        ),
    ]
