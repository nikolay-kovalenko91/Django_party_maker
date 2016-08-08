# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-08 13:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserSocialProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_id', models.CharField(max_length=50)),
                ('social_first_name', models.CharField(max_length=50, null=True)),
                ('social_last_name', models.CharField(max_length=50, null=True)),
                ('social_photo_url', models.CharField(max_length=100, null=True)),
                ('social_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.SocialTypes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]