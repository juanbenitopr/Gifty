# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth import logout, login, authenticate

from gifts.forms import ListGiftForm
from gifts.models import List, GiftsMember, PUBLIC, LikeGiftProfile
from users.forms import LoginForm, NewUserForm, ProfileForm
from users.models import Profile, LikesUser


class CreateUser(View):

    def get(self,request):

        form_user = NewUserForm()

        context = {
            'form_user' : form_user
        }
        return render(request,'users/create.html',context)

    def post(self,request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mail = form.cleaned_data.get('mail')
            gender = form.cleaned_data.get('gender')
            name_profile = form.cleaned_data.get('name_profile')
            name_list = form.cleaned_data.get('name_list')
            age = form.cleaned_data.get('age')
            user = User.objects.create_user(username,mail,password)
            user.is_active = True
            user.is_staff = False
            user.save()
            profile = Profile.objects.create(owner = user,name = name_profile,age=age,gender=gender,is_default=True)
            profile.save()
            list = List.objects.create(user=user,profile=profile,name=name_list)
            list.save()
            likes = form.data.get("myTags")
            likes_list = likes.split(',')
            for like in likes_list:
                LikesUser.objects.create(like=like,user=user,profile=profile)
            return redirect(request.GET.get('next','login'))


class LoginView(View):

    def get(self,request):

        form = LoginForm()
        context = {
            'form_user':form
        }

        return render(request,'users/login.html',context)

    def post(self,request):
        error_messages = []
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is None:
                error_messages.append('Contraseña o usuario incorrectos')
            else:
                if user.is_active:
                    login(request,user)
                    return redirect(request.GET.get('next','home'))
                else:
                    error_messages.append('Lo siento tu usuario no está activo')
        context = {
            'errors' : error_messages,
            'form_user' : form
        }
        return render(request,'users/login.html',context)

class LogoutView(View):

    @method_decorator(login_required())
    def get(self,request):
        if request.user.is_authenticated():
            logout(request)
        return redirect('home')

class ProfileView(View):

    @method_decorator(login_required())
    def get(self,request):

        profile = Profile.objects.order_by('-created_at').filter(owner = request.user).select_related('owner')
        form = ProfileForm()
        context = {
            'profiles':profile,
            'form_profile':form
        }

        return render(request,'users/profile.html',context)

    @method_decorator(login_required())
    def post(self,request):
        profile_new = Profile()
        profile_new.owner = request.user
        form = ProfileForm(request.POST,instance=profile_new)
        if form.is_valid():
            form.save()
            like_list = form.data.get('myTags')
            like_split = like_list.split(",")
            for like in like_split:
                likes_user = LikesUser.objects.create(user = request.user,profile=profile_new,like = like)
                likes_user.save()
            name_list = form.cleaned_data.get('name')+'_List'
            list = List.objects.create(user=request.user,name=name_list,profile = profile_new,visibility=PUBLIC)
            list.save()
            form_profile = ProfileForm()
            context = {
                'form_profile':form_profile,
                'success_message':'Guardado!',
                'error':[]
            }
            return render(request,'users/profile.html',context)
        else:
            form_profile = ProfileForm()
            context = {
                'form_profile':form_profile,
                'success_message':'No se ha podido guardar!',
                'errors':form.errors
                }
            return render(request,'users/profile.html',context)

class SelfData(View):

    @method_decorator(login_required())
    def get(self,request):
        query_profile = Profile.objects.filter(owner=request.user)
        query_list = List.objects.filter(user=request.user)
        query_likes = LikesUser.objects.filter(user = request.user)
        context = {
            'gifts_list':query_list,
            'profiles':query_profile,
            'likes_user':query_likes
        }
        return render(request,'users/SelfData.html',context)

class OtherData(View):

    @method_decorator(login_required)
    def get(self,request,pk):
        other_user = User.objects.get(pk=pk)
        if other_user is None:
            return HttpResponse ('Usuario no encontrado')
        else:
            query_list = List.objects.filter(user=other_user)
            query_profile = Profile.objects.filter(owner = other_user)
            context = {
                'lists':query_list,
                'other_user':other_user,
                'profiles':query_profile
            }
            return render(request,'users/profile_other.html',context)

@login_required(login_url='users/login.html')
def addGiftLikeProfile(request):
    if request.method == 'POST':
        pass
    pass
