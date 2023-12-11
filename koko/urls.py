"""koko URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", views.helloView),

    path("login/", views.login, name='login'),#已测试
    path("login/headicon/", views.getlogheadicon, name='getlogheadicon'),#已测试

    path("read/", views.read, name='read'),#已测试
    path("search/", views.search, name='search'),#已测试
    path("detail/", views.detail, name='detail'),#已测试
    path("list/", views.getlist, name='list'),#已测试

    path("setting/headIcon/", views.headicon_change, name='headicon_change'),#已测试
    path("setting/nickname/", views.nickname_change, name='nickname_change'),#已测试
    path("setting/timeline/", views.timeline_change, name='timeline_change'),#已测试
    path("setting/record/", views.record_change, name='record_change'),#已测试

    path("wb/create/", views.wb_create, name='wb_create'),
    path("wb/remove/", views.wb_remove, name='wb_remove'),
    path("wb/info/", views.wb_info_change, name='wb_info_change'),
    path("wb/image/get/", views.wb_image_get, name='wb_image_get'),
    path("wb/image/set/", views.wb_image_set, name='wb_image_set'),
    path("wb/type/", views.wb_type, name='wb_type'),

    path("word/add/", views.word_add, name='word_add'),
    path("word/remove/", views.word_remove, name='word_remove'),

    path("friends/list/", views.friends_list, name="friends_list"),
    path("friends/uidsearch/", views.friends_uidsearch, name='friends_uidsearch'),
    path("friends/follow/", views.friends_follow, name='friends_follow'),
    path("friends/unfollow/", views.friends_unfollow, name='friends_unfollow'),
    path("friends/headicon/", views.friends_headicon, name='friends_headicon'),
    path("friends/namesearch/", views.friends_namesearch, name='friends_namesearch'),
    path("friends/info/", views.friends_info, name='friends_info'),
    path("friends/subscribe/", views.friends_subscribe, name='frineds_subscribe'),
    path("friends/unsubscribe/", views.friends_unsubscribe, name='friends_unsubsrcibe'),

    path("test/subscribeall/", views.test_subscribeall),         # deleted, no use, only test
]
