# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
		user = models.OneToOneField(User, related_name='profile')
		region  = models.CharField(max_length=50, null=True, blank=True)
		about   = models.TextField(null=True, default='', blank=True)
		avatar  = models.ImageField(upload_to='avatars', blank=True)	