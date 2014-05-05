from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, logout, login

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from words.models import Word

def auth(request):
	return render(request, 'users/auth.html')

def home(request):
	if not request.user.is_authenticated():
		if not request.POST:
			return HttpResponseRedirect(reverse('users:auth'))
		
		u = request.POST['username']
		p = request.POST['password']
		# try:
			# p = request.POST['password1']
		# except:
			# p = request.POST['password']

		user = authenticate(username=u, password=p)
		if user is not None:
			if user.is_active:
				login(request, user)
				error_msg = "User is valid, active and authenticated"
			else:
				error_msg = "The password is valid, but the account has been disabled!"
		else:
			error_msg = "The username and password were incorrect."
	else:
		user = request.user
		error_msg = ''
		
	word_list = Word.objects.filter(user=user)
	return render(request, 'users/home.html', {'user':user, 'error_msg':error_msg, 'word_list':word_list})

def signout(request):
	logout(request)
	return HttpResponseRedirect(reverse('users:auth'))

def register(request):
	form = UserCreationForm()
	return render(request, 'users/register.html', {'form':form})

def register_check(request):
	name = request.POST['username']
	p = request.POST['password1']
	p2 = request.POST['password2']
	# todo check p equal p2

	user = User.objects.create_user(name, '', p)
	user.save()

	user_auth = authenticate(username=name, password=p)
	if user_auth is not None:
		if user_auth.is_active:
			login(request, user_auth)

	return HttpResponseRedirect(reverse('users:home'))
