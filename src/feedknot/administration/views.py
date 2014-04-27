# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from administration.models import LoginMaster

logger = logging.getLogger('application')

@login_required
def index(request):
    try:
        LoginMaster.objects.get(user=request.user)
    except LoginMaster.DoesNotExist:
        logger.info("Call set_default_box")
        loginMaster = LoginMaster()
        loginMaster.set_default_box(request)

    return render(request,
                  'feedknot/Mypage.html')
