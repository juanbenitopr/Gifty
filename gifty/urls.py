"""
Copyright 2015-2016, Juan Benito Pacheco Rubio
    This file is part of Gifty.

    Gifty is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
"""


from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from gifts.views import HomeGifts, CreateGift, DetailGift, AddGiftToList, CreateList, search_gift, like_gift
from users.views import LoginView, CreateUser, LogoutView, ProfileView, SelfData, OtherData, SelfLists, SelfProfiles

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',HomeGifts.as_view(),name='home'),
    url(r'^login$',LoginView.as_view(),name='login'),
    url(r'^logout$',LogoutView.as_view(),name='logout'),
    url(r'^create_user$',CreateUser.as_view(),name='users_create'),
    url(r'^create_gift$',CreateGift.as_view(),name='create_gift'),
    url(r'^detail/(?P<pk>[0-9]+)$',DetailGift.as_view(),name='detail_gift'),
    url(r'^create_list$',CreateList.as_view(),name='create_list'),
    url(r'^create_profile$',ProfileView.as_view(),name='create_profile'),
    url(r'^other_data/(?P<pk>[0-9]+)$',OtherData.as_view(),name='other_data'),
    url(r'^guardar_gift$',AddGiftToList.as_view(),name='guardar_gift'),
    url(r'^self_data',SelfData.as_view(),name='self_data'),
    url(r'^self_lists',SelfLists.as_view(),name='self_lists'),
    url(r'^self_profiles',SelfProfiles.as_view(),name='self_profiles'),
    url(r'^search_gift',search_gift,name='search_gift'),
    url(r'^like_gift',like_gift,name='like_gift'),
    url(r'^Files/(?P<path>.*)$',serve,{'document_root': settings.MEDIA_ROOT})
]
