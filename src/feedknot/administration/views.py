# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from administration.models import LoginMaster

@login_required
def index(request):
    try:
        userInfo = LoginMaster.objects.get(user=request.user)
    except LoginMaster.DoesNotExist:
        userInfo = LoginMaster.objects.create(user=request.user, default_box_id=-1)

    userName = userInfo.user.username
    return render_to_response('feedknot/Mypage.html',
                              {'login_flg':'1','user_name':userName},
                              context_instance=RequestContext(request))

