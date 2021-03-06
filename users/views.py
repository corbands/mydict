# -*- coding: utf-8 -*-
import pdb

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login

from django.utils.decorators import method_decorator

from django.utils import timezone

from django.contrib.auth.decorators import login_required

from django.views.generic.base import View, TemplateView
from django.views.generic.edit import FormView

from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from PIL import Image, ImageOps

from emh.settings import MEDIA_ROOT
from emh import settings
from words.models import Word
from users.models import User

from users.forms import RegisterForm, EditProfileForm, MyAuthForm

class AuthView(FormView):
    template_name = 'users/auth.html'
    form_class    = MyAuthForm

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return redirect('users:account', username = form.user_cache.username)

    def form_invalid(self, form):
        context = {'auth_failed':form.errors.values(), 'form':form}
        return render(self.request, self.template_name, context)

class AccountView(View):
    """
    В этом view отображается список слов пользователя
    """
    def post(self, request, *args, **kwargs):
        username = kwargs.get('username')

        # TODO: вынести обработку в forms.py
        en = request.POST['english']
        ru = request.POST['russian']

        if len(en) != 0 or len(ru) != 0:
            w = Word(english=en, russian=ru, pub_date=timezone.now(), user=request.user)
            w.save()
        return redirect('users:account', username = username)

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        
        if not username:
            username = request.user.username
            
        user = get_user(username)    
	
        if not user:
            return redirect('users:auth')
        
        word_list = user.word_set.order_by('-id').values()
	can_edit = username == request.user.username

        paginator = Paginator(word_list, settings.WORDS_COUNT_ON_PAGE)
        page = request.GET.get('page')
        try:
        	words = paginator.page(page)
    	except PageNotAnInteger:
    		words = paginator.page(1)
        except EmptyPage:
    		words = paginator.page(paginator.num_pages)

        context = {'userdata':user, 'words':words, 'can_edit':can_edit}
        return render(request, 'users/account.html', context)

class AboutView(TemplateView):
    template_name = 'users/about.html'

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        username  = form.cleaned_data.get('username')
        password  = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')
        email     = form.cleaned_data.get('email')
        region    = form.cleaned_data.get('region')
        first_name = form.cleaned_data.get('first_name')
        last_name  = form.cleaned_data.get('last_name')
        about     = form.cleaned_data.get('about')

        user = self.create_user(username   = username,
                                password   = password,
                                email      = email,
                                first_name = first_name,
                                last_name  = last_name,
                                region     = region,
                                about      = about)

        if 'avatar' not in self.request.FILES:
            self.save_default_avatar(user)
        else:
            save_avatar(user, self.request)

        user.save()

        user_auth = authenticate(username=username, password=password)
        if user_auth is not None:
            if user_auth.is_active:
                login(self.request, user_auth)

        return redirect('users:account', username=username)

    def form_invalid(self, form):
        context = {'register_failed':form.errors.values(), 'form':form}
        return render(self.request, self.template_name, context)

    def save_default_avatar(self, user):
        default_avatar = MEDIA_ROOT + '/default.jpg'
        image = Image.open(default_avatar)
        if image.mode not in ("L", "RGB"):
            image = image.convert("RGB")

        imagefit = ImageOps.fit(image, (160, 160))
        imagefit.save(default_avatar, 'JPEG', quality=75)

        img_file = open(default_avatar, 'r')
        user.avatar.save('default_avatar.jpg', File(img_file))
        img_file.close()

class EditProfileView(View):
    template_name = 'users/profile_edit.html'

    def get(self, request, *args, **kwargs):
        form = EditProfileForm()
        can_edit = False
        if request.user and request.user.username == kwargs['username']:
            can_edit = True

        user = get_user(kwargs['username'])

	if not user:
	    return redirect('users:auth')
	
        return render(request, self.template_name, {'form': form, 'userdata':user, 'can_edit': can_edit})    

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user            = request.user
            user.first_name = form.cleaned_data['first_name']                                                           
            user.last_name  = form.cleaned_data['last_name']                                                                      
            user.region     = form.cleaned_data['region']
            user.about      = form.cleaned_data['about']

            if 'avatar' in self.request.FILES:
                save_avatar(user, request)
            user.save()
            
            return redirect('users:account', username = user.username)
        else:
            return render(request, self.template_name, {'form': form})


def signout(request):
    logout(request)
    return redirect('users:auth')


#---------------------------
# other methods
#---------------------------
def get_user(username):
    try:	
        return User.objects.get(username__iexact = username)
    except ObjectDoesNotExist:
        return None

def handle_uploaded_file(file):    

    destination = open(MEDIA_ROOT + "/" + file.name, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)

    destination.flush() 

    image = Image.open(destination.name)
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    # image = image.resize((200, 200), Image.ANTIALIAS)
    # image.save(destination.name, 'JPEG', quality=75)

    imagefit = ImageOps.fit(image, (160, 160))
    imagefit.save(destination.name, 'JPEG', quality=75)

    return destination

def save_avatar(user, request):

    img = handle_uploaded_file(request.FILES['avatar'])
    frm = img.name.split('.')
    ava_name = user.username + '.' + frm[-1]

    user.avatar.save(ava_name, File(img))
    img.close()
