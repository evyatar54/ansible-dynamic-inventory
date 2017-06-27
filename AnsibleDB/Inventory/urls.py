

from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^host/create/', views.create_host),
    url(r'^host/delete/', views.delete_host),
    url(r'^host/add_to_group/', views.add_host_to_group),
    url(r'^host/remove_from_group/', views.remove_host_from_group),
    url(r'^group/get_hosts', views.get_all_hosts_by_group),
    url(r'^group/get_all', views.get_all_groups),
    url(r'^group/create', views.create_group),
    url(r'^group/delete', views.delete_group),
    url(r'^inventory', views.inventory),
]
