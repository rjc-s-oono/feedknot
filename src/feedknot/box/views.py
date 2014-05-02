# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from box.models import Box
from feed.models import Article
from feed.models import Feed
from administration.models import LoginMaster
import common.views

import logging

logger = logging.getLogger('application')

@login_required
def commonEdit(request):

    user_id = request.user.id

    try:
        manage_kbn = int(request.POST['manage_kbn'])
    except Exception:
        manage_kbn = -1

    #ボックス追加
    if manage_kbn == 1:
        add_box(request)
    #ボックス削除
    elif manage_kbn == 2:
        del_box(request)
    #ボックス名編集
    elif manage_kbn == 3:
        edit_box_name(request)
    #優先度変更
    elif manage_kbn == 4:
        edit_box_priority(request)

    box_list = Box.objects.filter(user_id=user_id).order_by('box_priority')
    param = {'box_list' : box_list}

    return render(request,'feedknot/CommonEdit.html',param)

@login_required
def searchFeed(request):
    box_id = -1

    try:
        box_id = int(request.POST['box_id'])
    except Exception:
        return common.views.err(request)

    if box_id < 0:
        logger.error('[searchFeed] box_idが設定されていません。')
        return common.views.err(request)

    return render(request,'feedknot/SearchFeed.html',{'box_id':box_id})

# ボックス登録
def add_box(request):

    try:
        # フィード登録
        box = Box(box_name='新規ボックス', user_id=request.user.id)
        box.save()
    except Exception:
        # ボックスの登録失敗
        return common.views.err(request)

    return

# ボックス削除
def del_box(request):
    box_id = -1

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_box] box_idが設定されていません。')
            return common.views.err(request)
    except Exception:
        # リクエストパラメータの取得に失敗
        return common.views.err(request)

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        target_user = LoginMaster.objects.get(user=request.user)
        target_user.del_box(box_id)
    except Exception:
        # ボックスの削除失敗
        return common.views.err(request)

    return

# ボックス名変更
def edit_box_name(request):
    box_id = -1

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_box] box_idが設定されていません。')
            return common.views.err(request)
    except Exception:
        # リクエストパラメータの取得に失敗
        return common.views.err(request)

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        box = Box.objects.get(id=box_id, user_id=request.user.id)
        box.edit_box_name(request.POST['box_name']);
    except Exception:
        # ボックスの削除失敗
        return common.views.err(request)

    return

# ボックス優先度変更
def edit_box_priority(request):
    box_id = -1

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_box] box_idが設定されていません。')
            return common.views.err(request)
    except Exception:
        # リクエストパラメータの取得に失敗
        return common.views.err(request)

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        box = Box.objects.get(id=box_id, user_id=request.user.id)
        box.edit_box_priority(request.POST['box_priority']);
    except Exception:
        # ボックスの削除失敗
        return common.views.err(request)

    return