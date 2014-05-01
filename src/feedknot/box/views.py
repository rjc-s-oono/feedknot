# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf, request
from django.http.response import HttpResponse
import json
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

    box_list = Box.objects.filter(user_id=user_id).order_by('box_priority')

    article_list = ''
#     for box in [box_list]:
#         article_list[request.box.id] = Article.objects.filter(box_id=request.box.id)

    param = {'user_id' : user_id,
         'article_list' : article_list,
         'box_list' : box_list}

    return render(request,'feedknot/CommonEdit.html',param)

#
#     try:
#         box_id = int(request.POST['box_id'])
#     except Exception:
#         box_id = -1
#
#     boxName = ""
#     if box_id > 0:
#         try:
#             boxInfo = Box.objects.get(id=box_id)
#             boxName = boxInfo.box_name
#             boxInfo.readFeed()
#         except ObjectDoesNotExist:
#             boxName = "ボックスが登録されていません。"
#     else:
#         try:
#             loginInfo = LoginMaster.objects.get(user=request.user)
#
#
#             box_id = loginInfo.default_box_id
#             boxInfo = Box.objects.get(id=box_id)
#             boxName = boxInfo.box_name
#             boxInfo.readFeed()
#         except ObjectDoesNotExist:
#             boxName = "ボックスが登録されていません。"
#
#     article_list = Article.objects.filter(box_id=box_id).order_by('-pub_date', 'id')
#     box_list = Box.objects.filter(user_id=user_id).order_by('box_priority')
#
#     param = {'user_id' : user_id,
#          'box_name' : boxName,
#          'article_list' : article_list,
#          'box_list' : box_list}
#     param.update(csrf(request))
#
#     return render_to_response('feedknot/CommonEdit.html',{})

@login_required
def searchFeed(request):
    box_id = -1

    # ユーザID取得
    if not request.user.is_authenticated():
        logger.error('[searchFeed] ユーザが存在しません。')
        return common.views.err(request)

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
    box_name = ''
    user_id = -1

    # ユーザID取得
    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        logger.error('[add_box] ユーザが存在しません。')
        return common.views.err(request)

    box_name = 'デフォルト'

    try:
        # フィード登録
        box = Box(box_name=box_name, user_id=user_id)
        box.save()
    except Exception:
        # ボックスの登録失敗
        return HttpResponse(json.dumps({'result': 'regist box faild.'}),
                            mimetype='application/json')

    #res = json.dumps({'result': 'success', 'box_name': box_name})
    #res.update(csrf(request))

    #return HttpResponse(res, mimetype='application/json')
    return

# ボックス削除
def del_box(request):
    box_id = -1
    user_id = -1

    # ユーザID取得
    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        logger.error('[del_box] ユーザが存在しません。')
        return common.views.err(request)

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_box] box_idが設定されていません。')
            return common.views.err(request)
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(
                json.dumps({
                'result': 'get param faild.[box_id=' +
                box_id + ',user_id=' + user_id + ']'}),
                mimetype='application/json')

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        Box.objects.filter(id=box_id, user_id=user_id).delete()
        Feed.objects.filter(box_id=box_id, user_id=user_id).delete()
        Article.objects.filter(box_id=box_id, user_id=user_id).delete()
    except Exception:
        # ボックスの削除失敗
        return HttpResponse(json.dumps({'result': 'delete box faild.'}),
                            mimetype='application/json')

    res = json.dumps({'result': 'success', 'box_id': box_id})
    #res.update(csrf(request))

    return HttpResponse(res, mimetype='application/json')

# ボックス名変更
def edit_box_name(request):
    box_id = -1
    user_id = -1

    # ユーザID取得
    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        logger.error('[del_box] ユーザが存在しません。')
        return common.views.err(request)

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_box] box_idが設定されていません。')
            return common.views.err(request)
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(
                json.dumps({
                'result': 'get param faild.[box_id=' +
                box_id + ',user_id=' + user_id + ']'}),
                mimetype='application/json')

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        box = Box.objects.get(id=box_id)
        box.box_name = request.POST['box_name']
        box.save()
    except Exception:
        # ボックスの削除失敗
        return HttpResponse(json.dumps({'result': 'delete box faild.'}),
                            mimetype='application/json')

    res = json.dumps({'result': 'success', 'box_id': box_id})
    #res.update(csrf(request))

    return HttpResponse(res, mimetype='application/json')
