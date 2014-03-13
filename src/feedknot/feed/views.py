from django.core.context_processors import csrf, request
from django.shortcuts import render_to_response
from box.models import Box
from feed.models import Article
from feed.models import Feed
from administration.models import LoginMaster
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import json
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

# TMP：日付関数ができるまでのとりあえずimport
import datetime
import locale
import re

@login_required
def main(request):

    user_id=request.user.id
    box_id = -1

    print('user_id')
    print(user_id)

    try:
        box_id = int(request.POST['box_id'])
    except Exception:
        box_id = -1

    boxName = ""
    if box_id > 0:
        try:
            boxInfo = Box.objects.get(id=box_id)
            boxName = boxInfo.box_name
            boxInfo.readFeed()
        except ObjectDoesNotExist:
            boxName = "ボックスが登録されていません。"
    else:
        try:
            loginInfo = LoginMaster.objects.get(user=request.user)
            box_id = loginInfo.default_box_id
            boxInfo = Box.objects.get(id=box_id)
            boxName = boxInfo.box_name
            boxInfo.readFeed()
        except ObjectDoesNotExist:
            boxName = "ボックスが登録されていません。"

    article_list = Article.objects.filter(box_id=box_id).order_by('-pub_date', 'id')
    box_list = Box.objects.filter(user_id=user_id).order_by('box_priority')

    param = {'user_id' : user_id,
         'box_name' : boxName,
         'article_list' : article_list,
         'box_list' : box_list}
    param.update(csrf(request))

    return render_to_response('feedknot/main.html',
                               param)


# フィード追加(ajax)
def add_feed(request):
    box_id = -1
    user_id = 1
    rssaddress = ''
    title = ''
    className = ''

    if not request.is_ajax():
        # Ajaxではない為エラー
        return HttpResponse(json.dumps({'result': 'request is not ajax.'}), mimetype='application/json')

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
        rssaddress = request.POST['url']
        title = request.POST['title']
        className = request.POST['className']
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(json.dumps({
                'result': 'getting param faild.[box_id=' +
                box_id + ',rssaddress=' + rssaddress + ',title=' + title + ']'}),
                mimetype='application/json')

    try:
        # フィード登録
        feed = Feed(box_id=box_id, user_id=user_id,
                    rss_address=rssaddress,feed_priority=3,last_take_date=datetime.datetime.today())
        feed.save()
    except Exception:
        # フィードの登録失敗
        return HttpResponse(json.dumps({'result': 'regist feed faild.'}), mimetype='application/json')

    # タグを一時的に削除
    # のちのちdivかなんかのメッセージウィンドウで表示すると思うので、その時に消します
    title = re.sub(r'</*[bBuU]>', '', title)

    res = json.dumps({'result': 'success', 'title': title, 'className': className})
    #res.update(csrf(request))

    return HttpResponse(res, mimetype='application/json')


# フィード削除(ajax)
def del_feed(request):
    box_id = -1
    user_id = 1
    feed_id = 1

    if not request.is_ajax():
        # Ajaxではない為エラー
        return HttpResponse(json.dumps({'result': 'request is not ajax.'}), mimetype='application/json')

    # ユーザID取得
    if request.user.is_authenticated():
        user_id=request.user.id
    else:
        user_id=1

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            box_id = 1
        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            feed_id = 1
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(json.dumps({
                'result': 'getting param faild.[box_id=' +
                str(box_id) + ',user_id=' + str(user_id) + ',feed_id=' + str(feed_id) + ']'}),
                mimetype='application/json')

    # フィード削除
    try:
        Feed.objects.filter(box_id=box_id, user_id=user_id, id=feed_id).delete()
    except Exception:
        # フィードの削除失敗
        return HttpResponse(json.dumps({'result': 'delete feed faild.[box_id=' +
                str(box_id) + ',user_id=' + str(user_id) + ',feed_id=' + str(feed_id) + ']'}), mimetype='application/json')

    return HttpResponse(json.dumps({'result': 'success', 'feed_id': feed_id}), mimetype='application/json')


# 記事既読更新(ajax)
def upd_article(request):
    box_id = -1
    user_id = 1
    feed_id = 1
    article_id = 1

    if not request.is_ajax():
        # Ajaxではない為エラー
        return HttpResponse(json.dumps({'result': 'request is not ajax.'}), mimetype='application/json')

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
        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            feed_id = 1
        if 'article_id' in request.POST and request.POST['article_id'].isdigit():
            article_id = int(request.POST['article_id'])
        else:
            article_id = 1
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(json.dumps({
                'result': 'getting param faild.[box_id=' +
                box_id + ',feed_id=' + feed_id + ',article_id=' + article_id + ']'}),
                mimetype='application/json')

    # 記事更新
    try:
        article = Article.objects.filter(box_id=box_id, user_id=user_id, feed_id=feed_id, id=article_id)
        article.read_flg = True
        article.save()
    except Exception:
        # 記事更新失敗
        return HttpResponse(json.dumps({'result': 'update article faild.'}), mimetype='application/json')

    # そのまま記事に遷移する為、何も返さない


# フィードのボックスID更新(ajax)
def change_box(request):
    box_id = -1
    user_id = 1
    feed_id = 1

    if not request.is_ajax():
        # Ajaxではない為エラー
        return HttpResponse(json.dumps({'result': 'request is not ajax.'}), mimetype='application/json')

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
        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            feed_id = 1
    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(json.dumps({
                'result': 'getting param faild.[box_id=' +
                box_id + ',feed_id=' + feed_id + ']'}),
                mimetype='application/json')

    # フィード更新
    try:
        feed = Feed.objects.filter(user_id=user_id, feed_id=feed_id)
        feed.box_id = box_id
        feed.save()
    except Exception:
        # フィード更新失敗
        return HttpResponse(json.dumps({'result': 'update feed(box_id) faild.'}), mimetype='application/json')

    return HttpResponse(json.dumps({'result': 'success', 'feed_id': feed_id}), mimetype='application/json')

