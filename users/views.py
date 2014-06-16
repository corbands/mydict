from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login

from django.utils import timezone

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from words.models import Word
from users.models import EmhUser

def auth(request):
    return render(request, 'users/auth.html')

def auth_check(request):
    u = request.POST['username']
    p = request.POST['password']
    if u == "" or p == "":
        context = {'auth_failed': "login or password are empty"}
        return render(request, 'users/auth.html', context)

    user = authenticate(username=u, password=p)

    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('users:home')

        else:
            msg = "The password is valid, but the account has been disabled!"
            context = {'auth_failed': msg}
            return render(request, 'users/auth.html', context)
    else:
        context = {'auth_failed':"login or password are incorrect!"}
        return render(request, 'users/auth.html', context)

@login_required
def home(request, page_number=0):
    page_number = int(page_number)    
    user = request.user

    if request.method == 'POST':
        if request.POST.__contains__('english') and request.POST.__contains__('russian'):
            en = request.POST['english']
            ru = request.POST['russian']

            if len(en) != 0 or len(ru) != 0:
                w = Word(english=en, russian=ru, pub_date=timezone.now(), user=request.user)
                w.save()

    word_list = Word.objects.filter(user=user)

    n = 20
    beg = 0
    if len(word_list) < n:
        end = len(word_list)
    else:    
        end = n    
    
    if page_number:                
        beg = n * (page_number)
        end = n * (page_number + 1)

    emh_user = EmhUser.objects.filter(user=user)
    
    context = {'emh_user':emh_user[0], 'word_list':word_list[beg:end], 'number_of_pages':range(1, len(word_list)/3 + 1)}
    return render(request, 'users/home.html', context)

def signout(request):
    logout(request)
    return redirect('users:auth')

def register(request):	
    return render(request, 'users/register.html')

def register_check(request):
    name = request.POST['username']
    p = request.POST['password1']
    p2 = request.POST['password2']
    a = request.POST['age']
    reg = request.POST['region']

    if p != p2:
        context = { 'register_failed': 'passwords not equal!' }
        return render(request, 'users/register.html', context)
    # todo check p equal p2

    user = User.objects.create_user(name, '', p)
    emh_user = EmhUser(user = user, age = a, region = reg)
    emh_user.save()
    user.save()

    user_auth = authenticate(username=name, password=p)
    if user_auth is not None:
        if user_auth.is_active:
            login(request, user_auth)

    return redirect('users:home')


def about(request):
    return render(request, 'users/about.html')


#private methods
