# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User

class Word(models.Model):
	english = models.CharField(max_length=50)
	russian = models.CharField(max_length=50)
	pub_date = models.DateTimeField('date published')

	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.english + u' — ' + self.russian

class Sentence(models.Model):
	english = models.CharField(max_length=140)
	russian = models.CharField(max_length=140)
	pub_date = models.DateTimeField('date published')	
