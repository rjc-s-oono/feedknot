# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from administration.models import LoginMaster
from django.core.exceptions import ObjectDoesNotExist

@login_required
def index(request):
    try:
        userInfo = LoginMaster.objects.get(user=request.user)
    except ObjectDoesNotExist:
        userInfo = LoginMaster.objects.create(user=request.user, default_box_id=-1)

    userName = userInfo.user.username
    return render_to_response('feedknot/Mypage.html',{'login_flg':'1','user_name':userName})

