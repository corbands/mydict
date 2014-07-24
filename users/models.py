# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser as _AbstractUser, UserManager as _UserManager


class UserManager(_UserManager):
	"""
	Менеджер модели пользователя "Словарика"
	"""
	def register(self, username, password, email, first_name, last_name, region, about, **extra_fields):

		#todo здесь нужно будет добавить проверку на уникальность email

		user = self.create_user(username   = username,
								password   = password,
								email      = email,
								first_name = first_name,
								last_name  = last_name,
								region     = region,
								about      = about,
								**extra_fields)
		return user



class AbstractUser(_AbstractUser):
	"""
	Абстракция модели пользователя "Словарика"
	"""
	region  = models.CharField(max_length = 50, null = True, blank = True)
	about   = models.TextField(null = True, default = '', blank = True)
	avatar  = models.ImageField(upload_to = 'avatars', blank = True)

	objects = UserManager()

	class Meta:
		abstract = True


class User(AbstractUser):
	"""
	Модель пользователя "Словарика"
	"""
	pass
