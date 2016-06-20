from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from rest_framework.response import Response
from django.template.defaulttags import register

from gifts.forms import GiftForm, CommentForm
from gifts.models import Gift, PUBLIC, GiftsMember, List, CommentGift, LikesGift, LikeGiftUser
from users.models import Profile, PhotoUser


class HomeGifts(View):


    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')
        gifts = Gift.objects.filter(visibility=PUBLIC).filter(~Q(user=request.user)).order_by('-created_at')
        profiles = Profile.objects.filter(user=request.user)
        lists = List.objects.filter(user = request.user )
        user_photo = PhotoUser.objects.filter(user=request.user)
        likes_user = {}
        if user_photo is None:
            user_photo = None
        for gift in gifts:
            user_like  = LikeGiftUser.objects.filter(user = request.user,gift=gift).count()
            likes_gift = LikeGiftUser.objects.filter(gift = gift).count()
            likes_user.update({gift.pk:[True if user_like>0 else False,likes_gift]})
        context = {
            'gifts_list':gifts,
            'profiles':profiles,
            'lists':lists,
            'user_photo':user_photo,
            'user_likes':likes_user
        }
        return render(request,'gifts/home.html',context)
    @method_decorator(login_required())
    def post(self,request):
        gift_owner = Gift()
        gift_owner.user = request.user
        form = GiftForm(request.POST, request.FILES, instance=gift_owner)
        if form.is_valid():
            form.save()
            profile = form.cleaned_data.get('profile')
            if profile is not None:
                list  = List.objects.filter(user=request.user,profile=form.cleaned_data.get('profile'))
            else:
                list  = List.objects.filter(user=request.user,profile=Profile.objects.filter(user = request.user,is_default=True))
            gift_list = GiftsMember.objects.create(gift=gift_owner,list =list[0])
            gift_list.save()
            gifts = Gift.objects.filter(visibility=PUBLIC).filter(~Q(user=request.user)).order_by('-created_at')
            profiles = Profile.objects.filter(user=request.user)
            form_create = GiftForm()
            form_create.fields.get('profile').queryset =  form_create.fields.get('profile').queryset.filter(user=request.user)
            context = {
                'gifts_list':gifts,
                'form_create':form_create,
                'profiles':profiles
            }
        else:
            context = {
                'error':form.errors
            }
        return  render(request,'gifts/home.html',context)

class CreateGift(View):

    @method_decorator(login_required())
    def post(self,request):
        if request.is_ajax() and request.POST:
            objects_upload = request.POST
            likes = objects_upload.get('caracteristicas').split(',')
            list_pk = objects_upload.get('list')
            list = List.objects.filter(pk=list_pk)[0]
            gift = Gift.objects.create(url=objects_upload.get('url'),tienda = objects_upload.get('tienda'), name=objects_upload.get('name'),user = request.user,photo=request._files.get('photo'),description=objects_upload.get('description'),prize = objects_upload.get('precio'),visibility=objects_upload.get('visibility'))
            GiftsMember.objects.create(gift=gift,list = list)
            for like in likes:
                LikesGift.objects.create(gift = gift,like = like)
            return HttpResponse('Conseguido')

class DetailGift(View):

    def get(self,request,pk):
         gift_possible = Gift.objects.filter(pk=pk)

         gift = gift_possible[0] if len(gift_possible)>0 else None
         if gift is not None:
             form  = CommentForm()
             comments = CommentGift.objects.filter(gift=gift)
             lists = List.objects.filter(user=request.user)
             user_photo = PhotoUser.objects.filter(user=request.user)
             if user_photo is None:
                 user_photo = None
             context = {
                 'gift':gift,
                 'form_coment':form,
                 'comments':comments,
                 'lists':lists,
                 'user_photo':user_photo
             }
             return render(request,'gifts/detail_gift.html',context)
         else:
             return HttpResponse('No se ha encontrado la foto')
    def post(self,request,pk):
        comment = CommentGift()
        comment.user = request.user
        gift = Gift.objects.filter(pk=pk)[0]
        comment.gift =gift
        form = CommentForm(request.POST,instance=comment)
        if form.is_valid:
            form.save()
            form  = CommentForm()
            comments = CommentGift.objects.filter(gift=gift)
            context = {
                'gift':gift,
                'form_coment':form,
                'comments':comments
            }
            return render(request,'gifts/detail_gift.html',context)

class AddGiftToList(View):

     def post(self,request):

         if request.is_ajax() and request.POST:
             id_list = int(request.POST.get('id_list'))
             id_gift = int(request.POST.get('id_gift'))
             gift = Gift.objects.filter(pk=id_gift)[0]
             list = List.objects.filter(pk=id_list)[0]
             GiftsMember.objects.create(list=list,gift=gift)
             return HttpResponse('conseguido')

class CreateList(View):
    @method_decorator(login_required)
    def post(self,request):
        if request.is_ajax() and request.POST:
            name = request.POST.get('name')
            visibility = request.POST.get('visibility')
            List.objects.create(user=request.user,visibility=visibility,name=name)
            return HttpResponse('Conseguido')

def search_gift(request):
        datas = request.POST.get('caract').split(',')
        gifts = []
        ids = []
        for data in datas:
            gift =LikesGift.objects.filter(like=data).exclude(gift__pk__in = ids).select_related('gift')
            if len(gift) > 0:
                for gift_1 in gift:
                    ids.append(gift_1.gift.pk)
                    gifts.append(gift_1.gift)

        profiles = Profile.objects.filter(user=request.user)
        lists = List.objects.filter(user=request.user)
        user_photo = PhotoUser.objects.filter(user=request.user)
        likes_user= {}
        for gift in gifts:
            user_like  = LikeGiftUser.objects.filter(user = request.user,gift=gift).count()
            likes_gift = LikeGiftUser.objects.filter(gift = gift).count()
            likes_user.update({gift.pk:[True if user_like>0 else False,likes_gift]})
        context={
            'gifts_list': gifts,
            'profiles': profiles,
            'lists': lists,
            'user_photo': user_photo,
            'user_likes':likes_user
        }
        return render(request, 'gifts/home.html', context)
def like_gift(request):
    if request.is_ajax() and request.POST:
        datas = request.POST.get('id_gift')
        gift = Gift.objects.filter(pk = datas)
        if len(gift)>0:
            gift = gift[0]
            like_gift = LikeGiftUser.objects.filter(gift=gift, user=request.user)
            if len(like_gift)>0:
                like_gift.delete()
            else:
                LikeGiftUser.objects.create(user = request.user,gift = gift)
            return HttpResponse('Conseguido')
    return HttpResponse('Error')

@register.filter
def get_user_like(dictionary, key):
    return dictionary.get(key)[0]

@register.filter
def get_number_like(dictionary, key):
    return dictionary.get(key)[1]
