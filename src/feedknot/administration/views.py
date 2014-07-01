# -*- coding: utf-8 -*-
import logging

from common.decorators import ajax_view
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from administration.models import LoginMaster
from box.forms import EditDefaultBoxForm

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
                  'feedknot/mypage.html')

@ajax_view(FormClass=EditDefaultBoxForm ,login_required=True)
def edit_default_box(request):

    logger.debug("■■■■■")

    edit_default_box_form = EditDefaultBoxForm(request.POST)
    edit_default_box_form.is_valid()

    box_id = edit_default_box_form.cleaned_data['box_id']
    try:
        loginMaster = LoginMaster.objects.get(user=request.user)
        loginMaster.edit_default_box(request.user,box_id)
        result = {'result': 'success'}
    except LoginMaster.DoesNotExist:
        result = {'result': 'error'}
        logger.info("Call set_default_box")
        loginMaster = LoginMaster()
        loginMaster.set_default_box(request)

    logger.debug(result)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), mimetype='application/json')
