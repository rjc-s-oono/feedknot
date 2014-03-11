from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def commonEdit(request):
    return render_to_response('feedknot/CommonEdit.html',{})

@login_required
def searchFeed(request):
    return render_to_response('feedknot/SearchFeed.html',{})