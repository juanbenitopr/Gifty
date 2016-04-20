"""gifty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from gifts.views import HomeGifts, CreateGift, DetailGift, AddGiftToList, CreateList
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
    url(r'^Files/(?P<path>.*)$',serve,{'document_root': settings.MEDIA_ROOT})
]
