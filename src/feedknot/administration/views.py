# -*- coding: utf-8 -*-
import logging

from common.decorators import ajax_view
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from box.models import Box
from feed.models import Article, Feed


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
                      'feedknot/common_edit.html',
                      {'box_list' : [loginMaster.default_box],
                       'default_box_id' : loginMaster.default_box.id,
                       'box_priority_array': [3, 2, 1]
                       })


    #main(request)
    user = request.user
    logger.debug("user_id: %s" % (user.id))

    # ユーザの全ボックス取得
    box_list = Box.objects.filter(user=user).order_by('box_priority')

    try:
        logger.info("get default box id." )
        login_info = LoginMaster.objects.get(user=user)
        default_box = login_info.default_box
        box_info = Box.objects.get(pk=default_box.id)
        box_name = box_info.box_name
        box_info.read_feed()

        article_list = Article.objects.filter(box=box_info, user=user, del_flg=False).order_by('-pub_date', 'id')
    except LoginMaster.DoesNotExist or Box.DoesNotExist:
        if len(box_list) > 0:
            box_info =  box_list[0]
            box_name = box_info.box_name
            box_info.read_feed()

            article_list = Article.objects.filter(box=box_info, user=user, del_flg=False).order_by('-pub_date', 'id')
        else:
            box_name = "ボックスが登録されていません。"
            article_list = []

    param = {'box_name' : box_name,
             'box_list' : box_list,
             'article_list' : article_list}

    return render(request,
                  'feedknot/main.html',
                  param)





    #return render(request,
    #              'feedknot/main.html')

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




def logout(request):

    param = {}

    return render(request,
                  'account/logout.html',
                  param)

