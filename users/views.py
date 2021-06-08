from datetime import date

import hashlib

import jwt

import urllib

import os

from django.views import View

import django.conf

from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse

from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

from django.urls import reverse

from django.contrib import messages

from django.core.files import File

from django.core.files.temp import NamedTemporaryFile

from .helper import get_photo_lists

from .models import User, UserPhotos, Post, UserManager, Like

from .forms import UserCreationForm, UserRegisterForm, UserSignInForm

from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError

from blog.utils import generate_token

from django.core.mail import EmailMessage

from django.views.decorators.csrf import csrf_exempt

import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subj = 'Activate your account'
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
        })


    email = EmailMessage(subject=email_subj, body=email_body, from_email=django.conf.settings.EMAIL_FROM_USER,
    to=[user.email]
    )

    EmailThread(email).start()


def index(request):
    if not request.user.is_authenticated:
        register_form = UserRegisterForm()
        signIn_form = UserSignInForm()

        return redirect('users:login')

    else:
        return redirect('users:profile', user_id=request.user.id)


def login(request):
    if request.user.is_authenticated:
        return redirect('users:index')

    if request.method == "POST":
        form = UserSignInForm(request.POST or None)

        if form.is_valid():
            login = form.cleaned_data['login']
            password = hashlib.md5(form.cleaned_data['password'].encode()).hexdigest()

            user = User.objects.filter(login=login, password=password).first()

            if user is not None:
                encoded = str(jwt.encode({'login': login, 'password': password}, 'secret', algorithm='HS256'))
                user.token = encoded
                user.save()

                auth_login(request, user)

                return redirect('users:profile', user_id=user.id)

        else:
            return render(request, "login/index.html", {'signIn_form' : form})

        return HttpResponseRedirect(reverse('users:index'))

    signIn_form = UserSignInForm()
    form = {'signIn_form': signIn_form}

    return render(request, "login/index.html", form)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        form.confirm_password = request.POST['confirm_password']

        if form.is_valid():
            login = form.cleaned_data['login']
            password = hashlib.md5(form.cleaned_data['password'].encode()).hexdigest()
            email = form.cleaned_data['email']

            encoded = str(jwt.encode({'login': login, 'password': password}, 'secret', algorithm='HS256'))
            
            user = User.objects.create(login = login, email=email, password=password, token=encoded, created_at=date.today().strftime("%Y-%m-%d"))
            user.save()

            send_activation_email(user, request)

            return redirect('users:login')
        
        else:
            return render(request, "login/register.html", {'register_form' : form})

    if not request.user.is_authenticated:
        register_form = UserRegisterForm()
        form = {'register_form': register_form}

        return render(request, "login/register.html", form)
    
    else:
        return redirect('users:index')


def logout(request):
    auth_logout(request)

    return HttpResponseRedirect(reverse('users:index'))


def main(request):
    return render(request, "main/index.html")


def profile(request, user_id):
    try:
        user = User.objects.filter(id=user_id).first()
        profile_photos = UserPhotos.objects.filter(user_id=user).order_by('-id')[:4]
        profile_posts = Post.objects.filter(user_id=user).order_by('-id')

        profile_info = {
        'user': user, 'profile_photos': profile_photos,
        'profile_posts': profile_posts
        }

        return render(request, "main/profile.html", profile_info)
    
    except:
        return render(request, 'errors/user_not_found.html')


def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:index'))

    return render(request, "settings/settings.html")


@csrf_exempt
def change_avatar(request):
    if request.is_ajax() and request.method == 'POST':
        user = User.objects.filter(id=request.user.id).first()

        user.avatar.delete(save=True)
        user.avatar.save(str(request.FILES['avatar-input']), request.FILES['avatar-input'])
    
        user.save()

        return JsonResponse({'ok': True})


def photo_album(request, user_id):
    try:
        user = User.objects.filter(id=user_id)[0]

        _photos = UserPhotos.objects.filter(user_id=user).order_by('-id')

        photos = {'photos': _photos}

        return render(request, "main/photo_album.html", photos)

    except:
        return render(request, 'errors/user_not_found.html')


def add_photo(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:index'))

    user = User.objects.filter(id=request.user.id).first()

    new_photo = UserPhotos.objects.create(user_id=user, photo=request.FILES['add-photo'])
    new_photo.save()

    return redirect('users:photo_album', user_id=user.id)


class FindUsers(View):
    def get(self, request):
        return render(request, "main/find_users.html")

    def post(self, request):
        login_or_name = request.POST['login_or_name']

        users = User.objects.filter(login__contains = login_or_name)
        users = users.union(User.objects.filter(full_name__contains = login_or_name))

        result_users = {'result_users': users}

        return render(request, "main/find_users.html", result_users)


def activate_user(request, uidb64, token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        return redirect('users:index')

    return render(request, 'authentication/activate_failed.html', {
        'user': user,

    })


def abracadabra(request):
    return render(request, 'main/easter_egg.html')