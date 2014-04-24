# -*- coding: utf-8 -*-
import re
import datetime
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse

from django.core.exceptions import ObjectDoesNotExist

from common.utils import datetime_util

from administration.models import LoginMaster
from box.models import Box
from feed.models import Article, Feed
import common.views

# FIXME simplejsonを使用してください
import json

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
    defBoxExistFlg = True;
    if box_id > 0:
        try:
            boxInfo = Box.objects.get(id=box_id)
            boxName = boxInfo.box_name
            boxInfo.readFeed()
        except ObjectDoesNotExist:
            defBoxExistFlg = False
    else:
        try:
            loginInfo = LoginMaster.objects.get(user=request.user)
            box_id = loginInfo.default_box_id
            boxInfo = Box.objects.get(id=box_id)
            boxName = boxInfo.box_name
            boxInfo.readFeed()
        except ObjectDoesNotExist:
            defBoxExistFlg = False


    box_list_len = Box.objects.filter(user_id=user_id).count()
    box_list = Box.objects.filter(user_id=user_id).order_by('box_priority')

    if (not defBoxExistFlg):
        if box_list_len > 0:
            boxInfo =  box_list[0]
            boxName = boxInfo.box_name
            box_id = boxInfo.id
            boxInfo.readFeed()
        else:
            boxName = "ボックスが登録されていません。"

    article_list = Article.objects.filter(box_id=box_id).order_by('-pub_date', 'id')

    param = {'user_id' : user_id,
         'box_name' : boxName,
         'article_list' : article_list,
         'box_list' : box_list}

    return render(request,
                    'feedknot/main.html',
                    param)

@login_required
def get_feeds(request):

    user_id=request.user.id
    box_id = -1

    print('user_id')
    print(user_id)

    # リクエストのボックスID取得
    try:
        box_id = int(request.POST['box_id'])
    except Exception:
        box_id = -1

    print('box_id(request)')
    print(box_id)

    defBoxExistFlg = True
    # デフォルトボックスID取得
    if box_id < 0:
        try:
            loginInfo = LoginMaster.objects.get(user=request.user)
            box_id = loginInfo.default_box_id
        except ObjectDoesNotExist:
            defBoxExistFlg = False
            box_id = -1

    print('box_id(default)')
    print(box_id)

    if box_id < 0:
        print('[get_feeds] box_idが設定されていません。')
        return common.views.err(request)

    boxName = ""

    if (not defBoxExistFlg):
        try:
            boxInfo = Box.objects.get(id=box_id)
            boxName = boxInfo.box_name
            boxInfo.readFeed()
        except ObjectDoesNotExist:
            defBoxExistFlg = False

    if (not defBoxExistFlg):
        boxName = "ボックスが登録されていません。"

    feed_list = Feed.objects.filter(user_id=user_id,box_id=box_id).order_by('priority', 'id')

    param = {'user_id' : user_id,
         'box_name' : boxName,
         'feed_list' : feed_list}

    return render(request,
                    'feedknot/main.html',
                    param)

# フィード追加(ajax)
def add_feed(request):
    box_id = -1
    user_id = -1
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
        print('[add_feed] ユーザが存在しません。')
        return HttpResponse(json.dumps({'result': 'user_id is not found.'}), mimetype='application/json')

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            print('[add_feed] box_idが設定されていません。')
            return HttpResponse(json.dumps({'result': 'box_id is not found.'}), mimetype='application/json')

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
        # 最初は2000年1月1日からのフィードを全て取得する
        today = datetime.date(2000, 1, 1)
        # TBD いつの日付設定かわからないので。。。(by sugano)
        # 下記で1日前取得できます。
        # one_days_ago = datetime_util.get_days_ago(today, 1)

        # フィード登録
        feed = Feed.objects.create(box_id=box_id, user_id=user_id,feed_name=title,
                    rss_address=rssaddress,feed_priority=3,last_take_date=today)
        feed.save()
    except Exception:
        # フィードの登録失敗
        return HttpResponse(json.dumps({'result': 'regist feed faild.'}), mimetype='application/json')

    # タグを一時的に削除
    # のちのちdivかなんかのメッセージウィンドウで表示すると思うので、その時に消します
    #title = re.sub(r'</*[bBuU]>', '', title)

    res = json.dumps({'result': 'success', 'title': title, 'className': className})
    #res.update(csrf(request))

    return HttpResponse(res, mimetype='application/json')


# フィード削除(ajax)
def del_feed(request):
    box_id = -1
    user_id = -1
    feed_id = -1

    #if not request.is_ajax():
        # Ajaxではない為エラー
        #return HttpResponse(json.dumps({'result': 'request is not ajax.'}), mimetype='application/json')

    # ユーザID取得
    if request.user.is_authenticated():
        user_id=request.user.id
    else:
        print('[del_feed] ユーザが存在しません。')
        return common.views.err(request)

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            print('[del_feed] box_idが設定されていません。')
            return common.views.err(request)

        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            print('[del_feed] feed_idが存在しません。')
            return common.views.err(request)
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
    user_id = -1
    feed_id = -1
    article_id = -1

    if not request.is_ajax():
        # Ajaxではない為エラー
        return HttpResponse(json.dumps({'result': 'request is not ajax.'}), mimetype='application/json')

    # ユーザID取得
    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        print('[upd_article] ユーザが存在しません。')
        return common.views.err(request)

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            print('[upd_article] box_idが設定されていません。')
            return common.views.err(request)

        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            print('[upd_article] feed_idが存在しません。')
            return common.views.err(request)

        if 'article_id' in request.POST and request.POST['article_id'].isdigit():
            article_id = int(request.POST['article_id'])
        else:
            print('[upd_article] article_idが存在しません。')
            return common.views.err(request)

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
    user_id = -1
    feed_id = -1

    if not request.is_ajax():
        # Ajaxではない為エラー
        return HttpResponse(json.dumps({'result': 'request is not ajax.'}), mimetype='application/json')

    # ユーザID取得
    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        print('[change_box] ユーザが存在しません。')
        return common.views.err(request)

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            print('[change_box] box_idが設定されていません。')
            return common.views.err(request)

        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            print('[change_box] feed_idが存在しません。')
            return common.views.err(request)

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

def feed_list(request):
    user_id=request.user.id
    box_id = -1

    print('user_id')
    print(user_id)

    try:
        manage_kbn = int(request.POST['manage_kbn'])
    except Exception:
        manage_kbn = -1

    #ボックス削除
    if manage_kbn == 1:
        del_feed(request)

    # リクエストのボックスID取得
    try:
        box_id = int(request.POST['box_id'])
    except Exception:
        return common.views.err(request)

    print('box_id(request)')
    print(box_id)

    if box_id < 0:
        print('[get_feeds] box_idが設定されていません。')
        return common.views.err(request)

    boxName = ""

    try:
        boxInfo = Box.objects.get(id=box_id)
        boxName = boxInfo.box_name
    except ObjectDoesNotExist:
        return common.views.err(request)

    feed_list = Feed.objects.filter(user_id=user_id,box_id=box_id).order_by('feed_priority', 'id')

    param = {'user_id' : user_id,
             'box_name' : boxName,
             'box_id' : box_id,
             'feed_list' : feed_list}

    return render(request,
                    'feedknot/feed.html',
                    param)
