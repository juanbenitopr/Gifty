# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.deletion import CASCADE

from users.models import Profile

PUBLIC  = "PUB"
PRIVATE = "PRIV"

LICENSES = (
    (PUBLIC,"Public"),
    (PRIVATE,"Private")
)
class Gift(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='gifts')
    description = models.TextField(blank=True,null=True,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    prize = models.FloatField()
    visibility = models.CharField(max_length=4,choices=LICENSES,default=PUBLIC)
    tienda = models.CharField(max_length=150,null=True)
    url = models.URLField(null=True)
    def __unicode__(self):
        return self.name

class GiftsCharts(models.Model):
    gift = models.ForeignKey(Gift)
    char = models.CharField(max_length=150)

class List(models.Model):
    name = models.CharField(max_length=150,default='')
    user = models.ForeignKey(User)
    gifts = models.ManyToManyField(Gift,through='GiftsMember',through_fields=('list','gift'))
    visibility = models.CharField(max_length=4,choices=LICENSES,default=PUBLIC)
    def __unicode__(self):
        return self.name

class GiftsMember (models.Model):
    gift = models.ForeignKey(Gift)
    list = models.ForeignKey(List)


class CommentGift(models.Model):
    comment = models.CharField(max_length=400)
    user = models.ForeignKey(User)
    gift = models.ForeignKey(Gift)

class ScoreGift(models.Model):
    score = models.IntegerField()
    gift = models.ForeignKey(Gift)
    user = models.ForeignKey(User)

class LikeGiftProfile(models.Model):
    profile = models.ForeignKey(Profile)
    list = models.ForeignKey(List)
    gift = models.ForeignKey(Gift)

class LikesGift(models.Model):
    like = models.CharField(max_length=150)
    gift = models.ForeignKey(Gift)
class LikeList(models.Model):
    like = models.CharField(max_length=150)
    list = models.ForeignKey(List)
