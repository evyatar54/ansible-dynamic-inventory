# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from collections import namedtuple
from django.shortcuts import render
from . import utils
import traceback,sys

Response = namedtuple("Response", ["success", "message", "data"])

@require_http_methods(["GET"])
def get_playbook(request):
    try:
        group_name = request.GET["groupname"]
        playbook = utils.generate_playbook(group_name)
        response = Response(success="True", message="Successfuly generated playbook", data=playbook)
    except KeyError:
        response = Response(success="False", message="missing argument: 'groupname'", data={})
    except Exception as e:
        response = Response(success="False", message=e.__str__(), data={})
    return JsonResponse(response._asdict())

@require_http_methods(["GET"])
def inventory(request):
    try:
        inventory = utils.get_inventory_json()
        response = Response(success="True", message="Successfuly fetched inventory", data=inventory)
    except Exception as e:
        response = Response(success="False", message=e.__str__(), data={})
    return JsonResponse(response._asdict())