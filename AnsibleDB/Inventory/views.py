# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from collections import namedtuple

from django.shortcuts import render
from . import utils

Response = namedtuple("Response", ["success", "message", "data"])


# Create your views here.
@require_http_methods(["POST"])
def create_host(request):
    try:
        host_name = request.GET['hostname']
        group_name = request.GET['groupname']

        utils.create_host(host_name, group_name)
        message_str = "The host " + host_name + " was created successfully and added to group " + group_name
        response = Response(success="True", message=message_str, data={})
    except AttributeError:
        response = Response(success="False", message="hostname and groupname required in HTTP request", data={})
    except Exception as e:
        response = Response(success="False", message=e.args, data={})

    return JsonResponse(response._asdict())


def deleteHost(request):
    host_name = ""
    response = Response(success="False", message="",data="")
    try:
        if request.method == "GET":
            host_name = request.GET.hostname
    except ValueError as e:
        raise ("not a GET request")

    try:
        utils.deleteHost(host_name)
        response["success"]="True"
        response["message"]="The host " + host_name + " deleted successfully"
    except ValueError as e:
        response[message]=e.strerror

    return JsonResponse(response)


def addHostToGroup(request):
    host_name = ""
    group_name = ""
    response = Response(success="False", message="",data="")
    try:
        if request.method == 'GET':
            host_name = request.GET.hostname
            group_name = request.GET.groupname
    except ValueError as e:
        raise ("not a GET request")

    try:
        utils.addHostToGroup(host_name, group_name)
        response["success"]="True"
        response["message"]="The host " + host_name + " was added successfully to group " + group_name
    except ValueError as e:
        response[message]=e.strerror

    return JsonResponse(response)


def removeHostFromGroup(request):
    host_name = ""
    group_name = ""
    response = Response(success="False", message="",data="")
    try:
        if request.method == 'GET':
            host_name = request.GET.hostname
            group_name = request.GET.groupname
    except ValueError as e:
        raise ("not a GET request")

    try:
        utils.removeHostFromGroup(host_name, group_name)
        response["success"]="True"
        response["message"]="The host " + host_name + " was removed successfully from group " + group_name
    except ValueError as e:
        response[message]=e.strerror

    return JsonResponse(response)


def getAllHostsByGroup(request):
    group_name = ""

    response = Response(success="False", message="",data="")
    try:
        if request.method == 'GET':
            group_name = request.GET.groupname
    except ValueError as e:
        raise ("not a GET request")

    try:
        all_hosts = utils.getAllHostsByGroup(group_name)
        response["success"]="True"
        response["message"]="got hosts successfully for group" + group_name
        response["data"]=all_hosts
    except ValueError as e:
        response[message]=e.strerror

    return JsonResponse(response)


def getAllGroups(request):

    try:
        all_groups = utils.getAllGroups()
        response["success"]="True"
        response["message"]="got all groups successfully"
        response["data"]=all_groups
    except ValueError as e:
        response[message]=e.strerror

    return JsonResponse(response)


def createGroup(request):
    group_name = ""
    response = Response(success="False", message="",data="")
    try:
        if request.method == 'GET':
            group_name = request.GET.groupname
    except ValueError as e:
        raise ("not a GET request")

    try:
        all_groups = utils.createGroup(group_name)
        response["success"]="True"
        response["message"]="created group " + group_name + " successfully"
    except ValueError as e:
        response[message]=e.strerror

    return JsonResponse(response)

def deleteGroup(request):
    group_name = ""
    response = Response(success="False", message="",data="")
    try:
        if request.method == 'GET':
            group_name = request.GET.groupname
    except ValueError as e:
        raise ("not a GET request")

    try:
        all_groups = utils.deleteGroup(group_name)
        response["success"]="True"
        response["message"]="deleted group " + group_name + " successfully"
    except ValueError as e:
        response[message]=e.strerror

    return JsonResponse(response)

