# -*- coding: utf-8 -*-
import pdb

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login

from django.utils.decorators import method_decorator

from django.utils import timezone

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView


from words.models import Word
from users.models import EmhUser
from users.forms import EmhUserForm, EmhUserRegisterForm, MyAuthForm

class AuthView(FormView):
    template_name = 'users/auth.html'
    form_class = MyAuthForm

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return redirect('users:account', username = form.user_cache.username)

    def form_invalid(self, form):
        context = {'auth_failed':form.errors.values(), 'form':form}
        return render(self.request, self.template_name, context)

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

    # todo здесь нужно paginator использовать
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


class AboutView(TemplateView):
    template_name = 'users/about.html'

# def about(request):
    # return render(request, 'users/about.html')

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = EmhUserRegisterForm

    def form_valid(self, form):
        username  = form.cleaned_data['username']
        password  = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']
        region    = form.cleaned_data['region']
        firstname = form.cleaned_data['first_name']
        lastname  = form.cleaned_data['last_name']
        about     = form.cleaned_data['about']

        if password != password2:
            context = { 'register_failed': 'Пароли не совпадают!' }
            return render(self.request, self.template_name, context)

        user = User.objects.create_user(username, '', password,
                                        first_name = firstname, last_name = lastname)
        emh_user = EmhUser(user = user, region = region, about = about)
        emh_user.save()
        user.save()

        user_auth = authenticate(username=username, password=password)
        if user_auth is not None:
            if user_auth.is_active:
                login(self.request, user_auth)

        return redirect('users:account', username=username)

    def form_invalid(self, form):
        pass

# todo можно использовать ModelForm
class EmhUserView(View):
    template_name = 'users/profile_edit.html'
    
    def get(self, request, *args, **kwargs):
        form = EmhUserForm
        can_edit = False
        if request.user and request.user.username == kwargs['username']:
            can_edit = True

        userinfo = get_user(kwargs['username'])
        #todo можно ли вносить изменения в профиль? для этого нужно знать для какого профиля мы смотрим эту страницу.
        return render(request, self.template_name, {'form': form, 'userinfo':userinfo, 'can_edit': can_edit})    

    def post(self, request, *args, **kwargs):
        form = EmhUserForm(request.POST)
        if form.is_valid():
            user            = request.user
            emh_user        = user.emhuser                        
            user.first_name = form.cleaned_data['first_name']                                                           
            user.last_name  = form.cleaned_data['last_name']                                                                      
            emh_user.region = form.cleaned_data['region']
            emh_user.about  = form.cleaned_data['about']            
            user.save()
            emh_user.save()
            return redirect('users:account', username = request.user)
        else:
            return render(request, self.template_name, {'form': form})



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

def username_logged(username):
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
