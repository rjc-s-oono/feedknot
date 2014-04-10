# -*- coding: utf-8 -*-
import logging
from django.template import RequestContext
from django.shortcuts import render

def err(request):
    return render(request,'error.html')

def err_500(request):
    return render(request,'500.html')
