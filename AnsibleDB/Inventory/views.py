# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render
from AnsibleDB.Inventory import utils

# Create your views here.
def createHost(request):
    utils.createHost(request)
    return HttpResponse("Hello world")