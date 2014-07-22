# -*- coding: utf-8 -*-
import pdb
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmhUserForm(forms.Form):
	first_name = forms.CharField(required = False)
	last_name  = forms.CharField(required = False)
	region     = forms.CharField(required = False)
	about      = forms.CharField(required = False)


def ForbiddenUsernameValidator(value):
	forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup', 
		'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator', 
		'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
		'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs', 
		'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
		'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads', 
		'contact', 'blogs', 'feed', 'feeds', 'faq', 'intranet', 'log', 'registration', 'search', 
		'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
		'follow', 'activity', 'questions', 'articles', 'network',]

	if value.lower() in forbidden_usernames:
		raise ValidationError('This is a reserved word.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')


class EmhUserRegisterForm(EmhUserForm):
	username  = forms.CharField()
	password  = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(EmhUserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsernameValidator)
		self.fields['username'].validators.append(InvalidUsernameValidator)

class MyAuthForm(AuthenticationForm):
	error_messages = {
        'invalid_login': ("Логин и/или пароль некорректны"),
        'inactive': ("Аккаунт отключен"),
    }
