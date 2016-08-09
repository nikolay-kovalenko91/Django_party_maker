# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager

class SocialTypes(models.Model):
    '''Social networks types, now vk.com only'''
    name = models.CharField(max_length=50)

class UserSocialProfile(models.Model):
    '''Users social networks profiles'''
    user = models.ForeignKey('auth.User')
    social_type = models.ForeignKey(SocialTypes, on_delete=models.CASCADE)
    social_id = models.CharField(max_length=50)
    social_first_name = models.CharField(max_length=50, null=True)
    social_last_name = models.CharField(max_length=50, null=True)
    social_photo_url = models.CharField(max_length=100, null=True)

class Poll(models.Model):
    '''The polls'''
    error_css_class = 'error'
    DRINKS = (
        ('v', 'Водка'),
        ('b', 'Пиво'),
        ('j', 'Сок'),
        ('w', 'Вино'),
        ('l', 'Вино'),
    )
    PRESENCE_STATUSES = (
        ('t', 'Приду'),
        ('f', "Не приду"),
    )
    user = models.ForeignKey('auth.User')
    drink = models.CharField(max_length=1, choices=DRINKS)
    presence = models.CharField(max_length=1, choices=PRESENCE_STATUSES)