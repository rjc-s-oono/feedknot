from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def commonEdit(request):
    return render_to_response('feedknot/CommonEdit.html',{})

@login_required
def searchFeed(request):
    ctxt = RequestContext(request, {})
    return render_to_response('feedknot/SearchFeed.html',ctxt)