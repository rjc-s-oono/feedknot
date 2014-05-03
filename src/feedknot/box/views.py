# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from box.models import Box
from administration.models import LoginMaster

logger = logging.getLogger('application')

@login_required
def commonEdit(request):

    user = request.user
    logger.debug("user_id: %s" % (user.id))

    if request.method == "POST":
        try:
            manage_kbn = int(request.POST['manage_kbn'])
        except Exception:
            manage_kbn = -1

        #ボックス追加
        if manage_kbn == 1:
            # XXX viewから他のview呼び出し禁止
            add_box(request)
        #ボックス削除
        elif manage_kbn == 2:
            # XXX viewから他のview呼び出し禁止
            del_box(request)
        #ボックス名編集
        elif manage_kbn == 3:
            # XXX viewから他のview呼び出し禁止
            edit_box_name(request)
        #優先度変更
        elif manage_kbn == 4:
            edit_box_priority(request)

    box_list = Box.objects.filter(user=user).order_by('box_priority')
    logger.debug(box_list)

    return render(request,
                  'feedknot/CommonEdit.html',
                  {'box_list' : box_list})

@login_required
def searchFeed(request):

    try:
        box_id = int(request.POST['box_id'])
    except Exception:
        return HttpResponseRedirect(reverse('common_error'))

    if box_id < 0:
        logger.error('[searchFeed] box_idが設定されていません。')
        return HttpResponseRedirect(reverse('common_error'))

    return render(request,
                  'feedknot/SearchFeed.html',
                  {'box_id':box_id})

# ボックス登録
@login_required
def add_box(request):

    try:
        # フィード登録
        box = Box(box_name="新規ボックス", user=request.user)
        box.save()
    except Exception:
        # ボックスの登録失敗
        return HttpResponseRedirect(reverse('common_error'))

    return

# ボックス削除
@login_required
def del_box(request):

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_box] box_idが設定されていません。')
            return HttpResponseRedirect(reverse('common_error'))
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponseRedirect(reverse('common_error'))

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        target_user = LoginMaster.objects.get(user=request.user)
        target_user.del_box(box_id)
    except Exception:
        # ボックスの削除失敗
        return HttpResponseRedirect(reverse('common_error'))

    return

# ボックス名変更
@login_required
def edit_box_name(request):

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_box] box_idが設定されていません。')
            return HttpResponseRedirect(reverse('common_error'))
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponseRedirect(reverse('common_error'))

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        box = Box.objects.get(id=box_id, user=request.user)
        box.edit_box_name(request.POST['box_name'])
    except Exception:
        # ボックスの削除失敗
        return HttpResponseRedirect(reverse('common_error'))

    return

# ボックス優先度変更
@login_required
def edit_box_priority(request):

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_box] box_idが設定されていません。')
            return HttpResponseRedirect(reverse('common_error'))
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponseRedirect(reverse('common_error'))

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        box = Box.objects.get(id=box_id, user=request.user)
        box.edit_box_priority(request.POST['box_priority']);
    except Exception:
        # ボックスの削除失敗
        return HttpResponseRedirect(reverse('common_error'))

    return
