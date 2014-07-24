# -*- coding: utf-8 -*-
import pdb
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from users.models import User

def ForbiddenUsernameValidator(value):
	forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup', 
		'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator', 
		'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
		'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs', 
		'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
		'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads', 
		'contact', 'blogs', 'feed', 'feeds', 'faq', 'intranet', 'log', 'registration', 'search', 
		'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
		'follow', 'activity', 'questions', 'articles', 'network', 'word',]

	if value.lower() in forbidden_usernames:
		raise ValidationError('This is a reserved word.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')



class RegisterForm(forms.ModelForm):
	"""
	Форма регистрации пользователя "Словарика"
	"""
	password = forms.CharField(widget = forms.PasswordInput())
	password2 = forms.CharField(widget = forms.PasswordInput())

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name',
				  'region', 'about', 'avatar']

  	def __init__(self, *args, **kwargs):
  		super(RegisterForm, self).__init__(*args, **kwargs)
  		self.fields['username'].validators.append(ForbiddenUsernameValidator)
  		self.fields['username'].validators.append(InvalidUsernameValidator)

  	# todo clean fields дополнить какие нужны будут при валидации
  	def clean_email(self):
  		email = self.cleaned_data.get('email')

  		# if not email:
  			# raise ValidationError('please enter the email')

		# if User.objects.filter(email__iexact = email).count() > 0:
			# raise ValidationError('user with this email already registered')			
		return email

	def clean_password2(self):
		password2 = self.cleaned_data.get('password2')

		if 'password' in self.cleaned_data and \
				self.cleaned_data.get('password') != password2:
			raise forms.ValidationError(u"Пароли не совпадают")

		return password2


class EditProfileForm(forms.ModelForm):
	"""
	Форма изменения профиля пользователя
	"""
	class Meta:
		model = User
		fields = [ 'first_name', 'last_name',
				  'region', 'about', 'avatar']


class MyAuthForm(AuthenticationForm):
	"""
	Форма аутентификации пользователя "Словарика"
	"""

	username = forms.CharField(max_length=254, error_messages = {'required': u'Поле "Логин" должно быть заполнено'})
	password = forms.CharField(label=("Password"), widget=forms.PasswordInput, error_messages = {u'required': u'Поле "Пароль" должно быть заполнено'})

	error_messages = {
        'invalid_login': ("Логин и/или пароль некорректны"),
        'inactive': ("Аккаунт отключен"),
    }

	def __init__(self, *args, **kwargs):
		super(MyAuthForm, self).__init__(*args, **kwargs)
