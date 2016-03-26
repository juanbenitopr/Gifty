from __future__ import unicode_literals

from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.

HOMBRE = 'HOMB'
MUJER = 'MUJ'

GENDER = (
     (HOMBRE,'Hombre'),
     (MUJER,'Mujer')
)
class Profile(models.Model):
     name = models.CharField(max_length=150)
     owner = models.ForeignKey(User)
     created_at = models.DateTimeField(auto_now_add=True)
     is_default = models.BooleanField(default=False)
     gender = models.CharField(max_length=4,choices=GENDER,default=HOMBRE)
     age = models.IntegerField()
     def __unicode__(self):
         return self.name

class LikesUser(models.Model):
     profile = models.ForeignKey(Profile)
     like = models.CharField(max_length=150)

class Followers(models.Model):
    follower_owner= models.ForeignKey(User, related_name='+')
    follower_follow = models.ForeignKey(User,related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)

class Followed(models.Model):
    followed_owner = models.ForeignKey(User,related_name='+')
    followed_follow = models.ForeignKey(User,related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)