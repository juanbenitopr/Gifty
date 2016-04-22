from django.contrib import admin

# Register your models here.
from users.models import LikesUser, Profile, Followers, Followed, PhotoUser

admin.site.register(LikesUser)
admin.site.register(Profile)
admin.site.register(Followers)
admin.site.register(Followed)
admin.site.register(PhotoUser)
