from __future__ import absolute_import

from django.conf.urls import url
from django.contrib import admin

from . import views

admin.autodiscover()


urlpatterns = [
    url(r'^$', views.index, name='index'),
]