
from django import forms

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

    class Meta:
        model = CommentGift
        exclude = ['user','gift']