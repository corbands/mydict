# -*- coding: utf-8 -*-
import pdb

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login

from django.utils.decorators import method_decorator

from django.utils import timezone

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.views.generic.base import View
from django.views.generic.edit import FormView

from words.models import Word
from users.models import EmhUser

def auth(request):
    return render(request, 'users/auth.html')

def auth_check(request):
    # pdb.set_trace()    
    u = request.POST['username']
    p = request.POST['password']
    if u == "" or p == "":
        context = {'auth_failed': "Поля логин и/или пароль не заполнены"}
        return render(request, 'users/auth.html', context)

    user = authenticate(username=u, password=p)

    if user:
        if user.is_active:
            login(request, user)
            return redirect('users:account', username=user.username)

        else:
            msg = "The password is valid, but the account has been disabled!"
            context = {'auth_failed': msg}
            return render(request, 'users/auth.html', context)
    else:
        context = {'auth_failed':"Логин и/или пароль некорректны"}
        return render(request, 'users/auth.html', context)

@login_required
def account(request, username='', page_number=1):
    if username and not username_logged(username):
        raise Http404

    page_number = int(page_number)
    user = get_user(username)

    if request.method == 'POST':
        if request.POST.__contains__('english') and request.POST.__contains__('russian'):
            en = request.POST['english']
            ru = request.POST['russian']

            if len(en) != 0 or len(ru) != 0:
                w = Word(english=en, russian=ru, pub_date=timezone.now(), user=request.user)
                w.save()

    word_list = Word.objects.filter(user=user)

    n = 5   # количество слов на одной странице по 3, 5, 10, 20
    beg, end = get_page_wordlist(page_number, word_list, n)

    emh_user = EmhUser.objects.filter(user=user)

    num_pages = len(word_list) / n
    if len(word_list) % n:
        num_pages += 1

    can_edit = username == request.user.username

    context = {'emh_user':emh_user[0], 'word_list':word_list[beg:end], 'pages':range(1, num_pages + 1), 'can_edit':can_edit}
    return render(request, 'users/account.html', context)

def signout(request):
    logout(request)
    return redirect('users:auth')

def register(request):
    return render(request, 'users/register.html')

def register_check(request):
    username  = request.POST['username']
    p         = request.POST['password1']       
    p2        = request.POST['password2']      
    a         = request.POST['age']             
    reg       = request.POST['region']        
    firstname = request.POST['firstname']
    lastname  = request.POST['lastname'] 
    about     = request.POST['about']

    if p != p2:
        context = { 'register_failed': 'passwords not equal!' }
        return render(request, 'users/register.html', context)

    user = User.objects.create_user(username, '', p, first_name=firstname, last_name=lastname)
    emh_user = EmhUser(user = user, age = a, region = reg, about = about)
    emh_user.save()
    user.save()

    user_auth = authenticate(username=name, password=p)
    if user_auth is not None:
        if user_auth.is_active:
            login(request, user_auth)

    return redirect('users:account', username=user.username)


def about(request):
    return render(request, 'users/about.html')

class EmhUserView(FormView):
    template_name = 'users/profile_edit.html'
    form_class = EmhUserForm
    success_url = 'users:account'
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
        # return super(EmhUserView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(EmhUserView, self).form_valid(form)

    # def get_success_url(self):
        # return reverse(success_url, username=request.user)

    # def get(self, request, *args, **kwargs):
    #     form = EmhUserForm()
    #     return render(request, self.template_name, {'form': form})    

    # def post(self, request, *args, **kwargs):
    #     form = EmhUserForm(request.POST)
    #     if form.is_valid:
    #         user            = request.user
    #         emh_user        = user.emhuser            
    #         user.first_name = request.POST['firstname']                                                           
    #         user.last_name  = request.POST['lastname']                                                                      
    #         emh_user.age    = request.POST['age']
    #         emh_user.region = request.POST['region']
    #         emh_user.about  = request.POST['about']
    #         emh_user.save()
    #         user.save()
    #         return redirect('users:account', username = request.user)
    #     else:
    #         return render(request, self.template_name, {'form':form})



#---------------------------
#private methods
#---------------------------
def get_page_wordlist(page_number, word_list, n):
    beg = 0
    if len(word_list) < n:
        end = len(word_list)
    else:
        end = n

    if page_number:
        page_number -= 1
        beg = n * (page_number)
        end = n * (page_number + 1)

    return [beg, end]

import pdb
def username_logged(username):
    # pdb.set_trace()
    users = EmhUser.objects.all()
    names = []
    for u in users:
        names.append(u.user.username)

    return username in names

def get_user(username):
    users = EmhUser.objects.all()
    names = []
    for u in users:
        if u.user.username == username:
            return u.user

    return None
