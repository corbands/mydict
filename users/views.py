from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, logout, login

from django.utils import timezone

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from words.models import Word

def auth(request):
    return render(request, 'users/auth.html')

def home(request):
    error_msg = ''
    msg_type = ''

    if not request.user.is_authenticated():
        if not request.POST:
            return HttpResponseRedirect(reverse('users:auth'))

        u = request.POST['username']
        p = request.POST['password']
        if u == "" or p == "":
            context = {'auth_failed':"login or password are empty"}
            return render(request, 'users/auth.html', context)

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
                msg_type = "warning"
        else:
            context = {'auth_failed':"login or password are incorrect!"}
            return render(request, 'users/auth.html', context)
    else:
        user = request.user

        if request.method == 'POST':
            if request.POST.__contains__('english') and request.POST.__contains__('russian'):
                en = request.POST['english']
                ru = request.POST['russian']
                w = Word(english=en, russian=ru, pub_date=timezone.now(), user=request.user)
                w.save()

    word_list = Word.objects.filter(user=user)

    context = {'user':user, 'error_msg':error_msg, 'msg_type':msg_type, 'word_list':word_list}
    return render(request, 'users/home.html', context)

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:auth'))

def register(request):	
    return render(request, 'users/register.html')

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


def about(request):
    return render(request, 'users/about.html')