

from django.conf.urls import re_path, include
from django.contrib import admin
from . import views

urlpatterns = [
    re_path(r'^host/create/$', views.create_host),
    re_path(r'^host/delete/$', views.delete_host),
    re_path(r'^host/add_to_group/$', views.add_host_to_group),
    re_path(r'^host/remove_from_group/$', views.remove_host_from_group),
    re_path(r'^group/get_hosts/$', views.get_all_hosts_by_group),
    re_path(r'^group/get_all/$', views.get_all_groups),
    re_path(r'^group/create/$', views.create_group),
    re_path(r'^group/delete/$', views.delete_group),
    re_path(r'^generate_playbook/$', views.get_playbook),
    re_path(r'^$', views.inventory),
]


"""
def get_host(hostname):
def get_all_hosts():
def get_host_roles(hostname):
def create_host(hostname, group_name):
def delete_host(hostname):
def remove_host_from_group(hostname, group_name):
def add_host_to_group(hostname, group_name):
def get_group_hosts(group_name):
def get_all_groups():
def get_all_platforms():
def create_group(group_name):
def delete_group(group_name):
def addGroupToGroup(hostname, group_name):
def getAllOSs():
def add_group_to_group(group_name, child_group_name):
def remove_group_child(group_name, child_group_name):
def get_group(group_name):
def get_group_children(group_name):
def add_var_to_group(key, value, group_name):
def remove_var_from_group(key, group_name):
def get_group_vars(group_name):
def get_role(role_name):
def get_roles():
def get_group_roles(group_name):
def create_role(role_name):
def delete_role(role_name):
def add_role_to_host(role_name, hostname):
def add_role_to_group(role_name, group_name):
def remove_role_from_host(role_name, hostname):
def remove_role_from_group(role_name, group_name):
def get_inventory_json():
def generate_playbook(group_name):

"""