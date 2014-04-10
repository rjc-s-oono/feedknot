# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render

from administration.models import LoginMaster
from box.models import Box

@login_required
def index(request):
    try:
        userInfo = LoginMaster.objects.get(user=request.user)
    except LoginMaster.DoesNotExist:
        userInfo = create(request)

    userName = userInfo.user.username

    return render(request,
                  'feedknot/Mypage.html',
                  {'login_flg':'1','user_name':userName})

# ログインマスタ登録 & デフォルトボックス登録
@login_required
def create(request):
    user = LoginMaster.objects.create(user=request.user, default_box_id=-1)
    box = Box.objects.create(box_name="デフォルトボックス",user_id=user.id)
    user.default_box_id = box.id
    user.save()
    return user
