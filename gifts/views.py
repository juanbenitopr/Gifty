from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
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
        form_create = GiftForm()
        context = {
            'gifts_list':gifts,
            'form_create':form_create
        }
        return render(request,'gifts/home.html',context)

class CreateGift(View):

    @method_decorator(login_required())
    def get(self,request):
        new_gift = GiftForm()
        new_gift.fields.get('profile').queryset =  new_gift.fields.get('profile').queryset.filter(owner=request.user)
        context = {
            'gifts_form':new_gift
        }
        return render(request,'gifts/create_gift.html',context)

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
            form = GiftForm()
            success_message = 'Guardado con exito'
            context = {
                'form':form,
                 'success_message':success_message
            }
        else:
            context = {
                'error':form.errors
            }
        return  render(request,'gifts/create_gift.html',context)

class DetailGift(View):

    def get(self,request,pk):
         gift_possible = Gift.objects.filter(pk=pk)

         gift = gift_possible[0] if len(gift_possible)>0 else None
         if gift is not None:
             form  = CommentForm()
             comments = CommentGift.objects.filter(gift=gift)
             context = {
                 'gift':gift,
                 'form_coment':form,
                 'comments':comments
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


@login_required(login_url='users/login.html')
def create_list(request):
    if request.method=='GET':
        List.created(user=request.user)
        return HttpResponse('Conseguido')
