# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth import logout, login, authenticate

from gifts.models import List,PUBLIC

from users.forms import LoginForm, NewUserForm
from users.models import Profile, LikesUser, PhotoUser


class CreateUser(View):

    def get(self,request):

        form_user = NewUserForm()

        context = {
            'form_user' : form_user
        }
        return render(request,'users/create.html',context)

    def post(self,request):
        form = NewUserForm(request.POST,request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            mail = form.cleaned_data.get('mail')
            gender = form.cleaned_data.get('gender')
            name_profile = form.cleaned_data.get('name_profile')
            name_list = form.cleaned_data.get('name_list')
            age = form.cleaned_data.get('age')
            photo_user = form.cleaned_data.get('photo')
            user = User.objects.create_user(username,mail,password)
            user.is_active = True
            user.is_staff = False
            user.save()
            profile = Profile.objects.create(owner = user,name = name_profile,age=age,gender=gender,is_default=True)
            profile.save()
            list = List.objects.create(user=user,profile=profile,name=name_list)
            list.save()
            if photo_user is not None:
                PhotoUser.objects.create(user = user,photo = photo_user)
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
    def post(self,request):
        if request.is_ajax() and request.POST:
            name_profile = request.POST.get('name')
            age_profile = request.POST.get('age')
            gender =request.POST.get('gender')
            profile_new = Profile.objects.create(name=name_profile,owner = request.user,gender=gender,age = age_profile)
            like_list = request.POST.get('like_list')
            like_split = like_list.split(",")
            for like in like_split:
                likes_user = LikesUser.objects.create(user = request.user,profile=profile_new,like = like)
                likes_user.save()
            name_list = name_profile+'_List'
            List.objects.create(user=request.user,name=name_list,profile = profile_new,visibility=PUBLIC)
            return HttpResponse('Conseguido')

class SelfData(View):
    @method_decorator(login_required())
    def get(self,request):
        query_profile = Profile.objects.filter(owner=request.user)
        query_list = List.objects.filter(user=request.user)
        query_likes = LikesUser.objects.filter(user = request.user)
        user_photo = PhotoUser.objects.filter(user=request.user)
        if user_photo is None:
            user_photo = None
        context = {
            'gifts_list':query_list,
            'profiles':query_profile,
            'likes_user':query_likes,
            'user_photo':user_photo
        }
        return render(request,'users/my_data.html',context)

class SelfLists(View):
    @method_decorator(login_required())
    def get(self,request):
        query_profile = Profile.objects.filter(owner=request.user)
        query_list = List.objects.filter(user=request.user)
        query_likes = LikesUser.objects.filter(user = request.user)
        user_photo = PhotoUser.objects.filter(user=request.user)
        if user_photo is None:
            user_photo = None
        context = {
            'gifts_list':query_list,
            'profiles':query_profile,
            'likes_user':query_likes,
            'user_photo':user_photo
        }
        return render(request,'users/lists.html',context)

class SelfProfiles(View):
    @method_decorator(login_required())
    def get(self,request):
        query_profile = Profile.objects.filter(owner=request.user)
        query_list = List.objects.filter(user=request.user)
        query_likes = LikesUser.objects.filter(user = request.user)
        user_photo = PhotoUser.objects.filter(user=request.user)
        if user_photo is None:
            user_photo = None
        context = {
            'gifts_list':query_list,
            'profiles':query_profile,
            'likes_user':query_likes,
            'user_photo': user_photo

        }
        return render(request,'users/profiles.html',context)

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

