
from django import forms
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _

from gifts.models import Gift, List, CommentGift


class GiftForm(forms.ModelForm):

    class Meta:
        model = Gift
        exclude = ['owners']

class ListGiftForm(forms.ModelForm):

    class Meta:
        model = List
        exclude = ['owner']

class CommentForm(forms.ModelForm):
    comment = CharField(label='Comentario', max_length=300)

    class Meta:
        model = CommentGift
        exclude = ['user','gift']
