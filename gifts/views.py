from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import View
from django.views.generic.detail import DetailView

from gifts.forms import GiftForm, CommentForm
from gifts.models import Gift, PUBLIC, GiftsMember, List, CommentGift
from users.models import Profile

class HomeGifts(View):


    def get(self,request):
        if not request.user.is_authenticated():
            return redirect('login')

        gifts = Gift.objects.filter(visibility=PUBLIC).filter(~Q(owners=request.user)).order_by('-created_at')
        profiles = Profile.objects.filter(owner=request.user)
        form_create = GiftForm()
        form_create.fields.get('profile').queryset =  form_create.fields.get('profile').queryset.filter(owner=request.user)
        context = {
            'gifts_list':gifts,
            'form_create':form_create,
            'profiles':profiles
        }
        return render(request,'gifts/home.html',context)
    @method_decorator(login_required())
    def post(self,request):
        gift_owner = Gift()
        gift_owner.owners = request.user
        form = GiftForm(request.POST, request.FILES, instance=gift_owner)
        if form.is_valid():
            form.save()
            profile = form.cleaned_data.get('profile')
            if profile is not None:
                list  = List.objects.filter(user=request.user,profile=form.cleaned_data.get('profile'))
            else:
                list  = List.objects.filter(user=request.user,profile=Profile.objects.filter(owner = request.user,is_default=True))
            gift_list = GiftsMember.objects.create(gift=gift_owner,list =list[0])
            gift_list.save()
            gifts = Gift.objects.filter(visibility=PUBLIC).filter(~Q(owners=request.user)).order_by('-created_at')
            profiles = Profile.objects.filter(owner=request.user)
            form_create = GiftForm()
            form_create.fields.get('profile').queryset =  form_create.fields.get('profile').queryset.filter(owner=request.user)
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
            profile_pk = objects_upload.get('profile')
            profile = Profile.objects.filter(pk=profile_pk)[0]
            list = List.objects.filter(profile=profile)[0]
            gift = Gift.objects.create(name=objects_upload.get('name'),profile=profile,owners = request.user,photo=request._files.get('photo'),description=objects_upload.get('description'),prize = objects_upload.get('precio'),visibility=objects_upload.get('visibility'))
            GiftsMember.objects.create(gift=gift,list = list)
            return HttpResponse('Conseguido')

class DetailGift(View):

    def get(self,request,pk):
         gift_possible = Gift.objects.filter(pk=pk)

         gift = gift_possible[0] if len(gift_possible)>0 else None
         if gift is not None:
             form  = CommentForm()
             comments = CommentGift.objects.filter(gift=gift)
             profiles = Profile.objects.filter(owner=request.user)
             context = {
                 'gift':gift,
                 'form_coment':form,
                 'comments':comments,
                 'profiles':profiles
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
             id_profile = int(request.POST.get('id_profile'))
             id_gift = int(request.POST.get('id_gift'))
             gift = Gift.objects.filter(pk=id_gift)[0]
             profile = Profile.objects.filter(pk=id_profile)
             list = List.objects.filter(user=request.user,profile=profile)[0]
             GiftsMember.objects.create(list=list,gift=gift)
             return HttpResponse('conseguido')

@login_required(login_url='users/login.html')
def create_list(request):
    if request.method=='GET':
        List.created(user=request.user)
        return HttpResponse('Conseguido')
