from django.shortcuts import render_to_response
from django.template.context import RequestContext

def commonEdit(request):
    return render_to_response('feedknot/CommonEdit.html',{})

def searchFeed(request):
    ctxt = RequestContext(request, {})
    return render_to_response('feedknot/SearchFeed.html',ctxt)