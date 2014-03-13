from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
import json
from box.models import Box
from feed.models import Article
from feed.models import Feed

@login_required
def commonEdit(request):
    return render_to_response('feedknot/CommonEdit.html',{})

@login_required
def searchFeed(request):
    ctxt = RequestContext(request, {})
    return render_to_response('feedknot/SearchFeed.html',ctxt)

# ボックス登録
def add_box(request):
    box_name = ''
    user_id = 1

    # ユーザID取得
    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        user_id = 1

    # リクエストパラメータ取得
    try:
        if 'box_name' in request.POST:
            box_name = request.POST['box_name']
        else:
            box_name = 'デフォルト'
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(
                json.dumps({
                'result': 'get param faild.[box_name=' +
                box_name + ',user_id=' + user_id + ']'}),
                mimetype='application/json')

    try:
        # フィード登録
        box = Box(box_name=box_name, user_id=user_id)
        box.save()
    except Exception:
        # ボックスの登録失敗
        return HttpResponse(json.dumps({'result': 'regist box faild.'}),
                            mimetype='application/json')

    res = json.dumps({'result': 'success', 'box_name': box_name})
    #res.update(csrf(request))

    return HttpResponse(res, mimetype='application/json')

# ボックス削除
def del_box(request):
    box_id = 1
    user_id = 1

    # ユーザID取得
    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        user_id = 1

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            box_id = 1
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(
                json.dumps({
                'result': 'get param faild.[box_id=' +
                box_id + ',user_id=' + user_id + ']'}),
                mimetype='application/json')

    # ボックス削除 (ボックスに割り当てられているフィードなども削除)
    try:
        Box.objects.filter(box_id=box_id, user_id=user_id).delete()
        Feed.objects.filter(box_id=box_id, user_id=user_id).delete()
        Article.objects.filter(box_id=box_id, user_id=user_id).delete()
    except Exception:
        # ボックスの削除失敗
        return HttpResponse(json.dumps({'result': 'delete box faild.'}),
                            mimetype='application/json')

    res = json.dumps({'result': 'success', 'box_id': box_id})
    #res.update(csrf(request))

    return HttpResponse(res, mimetype='application/json')
