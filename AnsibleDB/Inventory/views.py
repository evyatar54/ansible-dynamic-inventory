# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import *
from django.core.serializers.json import DjangoJSONEncoder

from collections import namedtuple

from django.shortcuts import render
from .utils import *

Response = namedtuple("Response", ["success","message","data"])

# Create your views here.
def createHost(request):
    host_name = ""
    group_name = ""
    response = Response(success="False", message="",data="")
    try:
        if request.method == "GET":
            host_name = request.GET.hostname
            group_name = request.GET.groupname
    except ValueError as e:

    try:
        utils.createHost(host_name, group_name)
        response["success"]="True"
        response["message"]="The host " + host_name + " added successfully"
    except ValueError as e:
        response[message]=e.strerror

    return HttpResponse(response)

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

    return HttpResponse(response)