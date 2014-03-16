# encoding: UTF-8
import logging
from django.template import RequestContext
from django.shortcuts import render_to_response

def err(request):
    return render_to_response('error.html',context_instance=RequestContext(request))

def err_500(request):
    return render_to_response('500.html',context_instance=RequestContext(request))
