from django.shortcuts import render_to_response

def commonEdit(request):
    return render_to_response('feedknot/CommonEdit.html',{})

def searchFeed(request):
    return render_to_response('feedknot/SearchFeed.html',{})