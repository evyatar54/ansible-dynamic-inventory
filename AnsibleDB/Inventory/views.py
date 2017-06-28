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


# Create your views here.
@require_http_methods(["POST"])
def create_host(request):
    try:
        host_name = request.GET['hostname']
        group_name = request.GET['groupname']

        utils.create_host(host_name, group_name)
        message_str = 'The host {}  was created successfully and added to group {}'\
            .format(host_name, group_name)
        response = Response(success="True", message=message_str, data={})
    except KeyError:
        response = Response(success="False",
                            message="hostname and groupname required in HTTP request", data={})
    except Exception as e:
        response = Response(success="False", message=e.args, data={})

    return JsonResponse(response._asdict())


@require_http_methods(["POST"])
def delete_host(request):
    try:
        host_name = request.GET['hostname']
        utils.deleteHost(host_name)
        response = Response(success="True",
                            message="host {} has been successfully removed".format(host_name), data={})
    except KeyError:
        response = Response(success="False",
                            message="hostname required in HTTP request", data={})
    except Exception as e:
        response = Response(success="False", message=e.args, data={})

    return JsonResponse(response)


@require_http_methods(["POST"])
def add_host_to_group(request):
    try:
        host_name = request.GET['hostname']
        group_name = request.GET['groupname']
        utils.addHostToGroup(host_name, group_name)
        response = Response(success="True", message="hostname has been successfully removed", data={})
    except KeyError:
        response = Response(success="False",
                            message="hostname and groupname required in HTTP request", data={})
    except Exception as e:
        response = Response(success="False", message=e.args, data={})

    return JsonResponse(response)


@require_http_methods(["POST"])
def remove_host_from_group(request):
    try:
        host_name = request.GET['hostname']
        group_name = request.GET['groupname']
        utils.removeHostFromGroup(host_name, group_name)
        response = Response(success="True",
                            message="{} has been successfully removed from group {}".format(host_name, group_name), data={})
    except KeyError:
        response = Response(success="False",
                            message="hostname and groupname required in HTTP request", data={})
    except Exception as e:
        response = Response(success="False", message=e.args, data={})

    return JsonResponse(response)


@require_http_methods(["GET"])
def get_all_hosts_by_group(request):
    try:
        group_name = request.GET['name']
        all_group_hosts = utils.get_all_hosts_by_group(group_name)
        response = Response(success="True",
                            message="got all '%s' group's successfully" % group_name,
                            data=all_group_hosts)
    except KeyError:
        response = Response(success="False", message="missing argument: 'name'", data={})
    except Exception as e:
        response = Response(success="False", message=e.__str__(), data={})
    return JsonResponse(response)


@require_http_methods(["GET"])
def get_all_groups(request):
    try:
        all_groups = utils.get_all_groups()
        response = Response(success="True", message="got all groups successfully", data=all_groups)
    except Exception as e:
        response = Response(success="True", message=e.__str__(), data={})
    return JsonResponse(response)


@require_http_methods(["POST"])
def create_group(request):
    try:
        group_name = request.POST['name']
        utils.create_group(group_name)
        response = Response(success="True", message="group '%s' created successfully" % group_name, data={})
    except KeyError:
        response = Response(success="False", message="missing argument: 'name'", data={})
    except Exception as e:
        response = Response(success="False", message=e.__str__(), data={})
    return JsonResponse(response)


@require_http_methods(["POST"])
def delete_group(request):
    try:
        group_name = request.POST['name']
        utils.delete_group(group_name)
        response = Response(success="True", message="group '%s' deleted successfully" % group_name, data={})
    except KeyError:
        response = Response(success="False", message="missing argument: 'name'", data={})
    except Exception as e:
        response = Response(success="False", message=e.__str__(), data={})

    return JsonResponse(response)


@require_http_methods(["GET"])
def inventory(request):
    try:
        inventory = utils.get_inventory_json()
        response = Response(success="True", message="Successfuly fetched inventory", data=inventory)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        response = Response(success="False", message=e.__str__(), data={})

    return JsonResponse(response._asdict())


@require_http_methods(["GET"])
def get_playbook(request):
    try:
        group_name = request.GET["groupname"]
        playbook = utils.generate_playbook(group_name)
        response = Response(success="False", message="Successfuly generated playbook", data=playbook)
    except KeyError:
        response = Response(success="False", message="missing argument: 'groupname'", data={})
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        response = Response(success="False", message=e.__str__(), data={})

    return JsonResponse(response._asdict())
