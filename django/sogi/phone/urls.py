# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'(^phone_info/$)', views.getPhoneInfo,name='phone_info'),
    url(r'^recommend/(?P<asp>.*)/$', views.getRecommend,name='recommend'),
    url(r'(^phone_info/other/$)', views.getTagSentence,name='other'),
    url(r'(^phone_info/percent/$)', views.getPercent,name='percent'),
]