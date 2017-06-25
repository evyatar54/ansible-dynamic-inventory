

from django.conf.urls import url, include
from django.contrib import admin
from AnsibleDB.Inventory import views

urlpatterns = [
    url(r'^createHost/', views.createHost),
    url(r'^removeHost/')
]
