# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-11 05:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('passes', models.BooleanField(default=False)),
                ('link', models.CharField(max_length=200)),
                ('cl_id', models.CharField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('processed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
