

from django.conf.urls import re_path, include
from django.contrib import admin
from . import views

urlpatterns = [
    re_path(r'^generate_playbook/$', views.get_playbook),
    re_path(r'^$', views.inventory),
]
