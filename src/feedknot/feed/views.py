# -*- coding: utf-8 -*-
import logging
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson

from common.decorators import ajax_view
#from common.utils import datetime_util

from administration.models import LoginMaster
from box.models import Box
from feed.models import Article, Feed

from feed.forms import AddFeedForm

logger = logging.getLogger('application')

@login_required
def main(request):

    user = request.user
    box_id = request.POST.get('box_id', '')

    logger.debug("user_id: %s" % (user.id))

    boxName = ""
    defBoxExistFlg = True;
    if box_id:
        try:
            boxInfo = Box.objects.get(id=box_id)
            boxName = boxInfo.box_name
            boxInfo.read_feed()
        except Box.DoesNotExist:
            defBoxExistFlg = False
    else:
        logger.info("get default box id." )
        try:
            loginInfo = LoginMaster.objects.get(user=user)
            default_box = loginInfo.default_box
            boxInfo = Box.objects.get(id=default_box.id)
            boxName = boxInfo.box_name
            boxInfo.read_feed()
        except LoginMaster.DoesNotExist or Box.DoesNotExist:
            defBoxExistFlg = False

    box_list = Box.objects.filter(user=user).order_by('box_priority')
    box_list_len = len(box_list)

    if (not defBoxExistFlg):
        if box_list_len > 0:
            boxInfo =  box_list[0]
            boxName = boxInfo.box_name
            box_id = boxInfo.id
            boxInfo.read_feed()
        else:
            boxName = "ボックスが登録されていません。"

    # XXX 正常系ではboxInfoを取得できるが、
    #     取れないパターンがあるとエラーになるので関数内のリファクタが必要
    article_list = Article.objects.filter(box=boxInfo).order_by('-pub_date', 'id')

    param = {'box_name' : boxName,
             'article_list' : article_list,
             'box_list' : box_list}

    return render(request,
                  'feedknot/main.html',
                  param)

@login_required
def get_feeds(request):

    # リクエストのボックスID取得
    try:
        box_id = int(request.POST['box_id'])
    except Exception:
        box_id = -1

    defBoxExistFlg = True
    # デフォルトボックスID取得
    if box_id < 0:
        try:
            loginInfo = LoginMaster.objects.get(user=request.user)
            default_box = loginInfo.default_box
            box_id = default_box.id
        except LoginMaster.DoesNotExist:
            defBoxExistFlg = False
            box_id = -1


    if box_id < 0:
        logger.error('[get_feeds] box_idが設定されていません。')
        return HttpResponseRedirect(reverse('common_error'))

    boxName = ""

    if (not defBoxExistFlg):
        try:
            boxInfo = Box.objects.get(id=box_id)
            boxName = boxInfo.box_name
            boxInfo.read_feed()
        except Box.DoesNotExist:
            defBoxExistFlg = False

    if (not defBoxExistFlg):
        boxName = "ボックスが登録されていません。"

    feed_list = Feed.objects.filter(user=request.user, box_id=box_id).order_by('priority', 'id')

    param = {'box_name' : boxName,
         'feed_list' : feed_list}

    return render(request,
                  'feedknot/main.html',
                  param)

# フィード追加(ajax)
@ajax_view(FormClass=AddFeedForm ,login_required=True)
def add_feed(request):

    add_feed_form = AddFeedForm(request.POST)
    add_feed_form.is_valid()

    box_id = add_feed_form.cleaned_data['box_id']
    rss_address = add_feed_form.cleaned_data['url']
    title = add_feed_form.cleaned_data['title']
    class_name = add_feed_form.cleaned_data['className']

    try:
        # ボックス取得
        box = Box.objects.get(id=box_id, user=request.user)

        # 最初は2000年1月1日からのフィードを全て取得する
        today = datetime.date(2000, 1, 1)

        # フィード登録
        feed = Feed(
            box = box,
            user = request.user,
            feed_name = title,
            rss_address = rss_address,
            feed_priority = 3,
            last_take_date = today,
        )
        feed.add_feed()

    except Exception:
        # フィードの登録失敗
        return HttpResponse(simplejson.dumps({'result': 'regist feed faild.'}, ensure_ascii=False), mimetype='application/json')

    # タグを一時的に削除
    # のちのちdivかなんかのメッセージウィンドウで表示すると思うので、その時に消します
    #title = re.sub(r'</*[bBuU]>', '', title)

    res = simplejson.dumps({'result': 'success', 'title': title, 'className': class_name}, ensure_ascii=False)

    return HttpResponse(res, mimetype='application/json')

# フィード削除(ajax)
def del_feed(request):

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[del_feed] box_idが設定されていません。')
            return HttpResponseRedirect(reverse('common_error'))

        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            logger.error('[del_feed] feed_idが存在しません。')
            return HttpResponseRedirect(reverse('common_error'))

    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(simplejson.dumps({
                'result': 'getting param faild.[box_id=' +
                str(box_id) + ',user_id=' + str(request.user.id) + ',feed_id=' + str(feed_id) + ']'}, ensure_ascii=False),
                mimetype='application/json')

    # フィード削除
    try:
        box = Box.objects.get(id=box_id, user=request.user)
        Feed.objects.filter(id=feed_id, box=box, user=request.user).delete()
    except Exception:
        # フィードの削除失敗
        return HttpResponse(simplejson.dumps({'result': 'delete feed faild.[box_id=' +
                str(box_id) + ',user_id=' + str(request.user.id) + ',feed_id=' + str(feed_id) + ']'}, ensure_ascii=False), mimetype='application/json')

    return HttpResponse(simplejson.dumps({'result': 'success', 'feed_id': feed_id}, ensure_ascii=False), mimetype='application/json')

# 記事既読更新(ajax)
@ajax_view(login_required=True)
def upd_article(request):

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[upd_article] box_idが設定されていません。')
            return HttpResponseRedirect(reverse('common_error'))

        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            logger.error('[upd_article] feed_idが存在しません。')
            return HttpResponseRedirect(reverse('common_error'))

        if 'article_id' in request.POST and request.POST['article_id'].isdigit():
            article_id = int(request.POST['article_id'])
        else:
            logger.error('[upd_article] article_idが存在しません。')
            return HttpResponseRedirect(reverse('common_error'))

    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(simplejson.dumps({
                'result': 'getting param faild.[box_id=' +
                box_id + ',feed_id=' + feed_id + ',article_id=' + article_id + ']'}, ensure_ascii=False),
                mimetype='application/json')

    # 記事更新
    try:
        box = Box.objects.get(id=box_id, user=request.user)
        feed = Feed.objects.get(id=feed_id, box=box, user=request.user)

        article = Article.objects.filter(id=article_id, box=box, feed=feed, useu=request.user)
        article.read_flg = True
        article.save()
    except Exception:
        # 記事更新失敗
        return HttpResponse(simplejson.dumps({'result': 'update article faild.'}, ensure_ascii=False), mimetype='application/json')

    # そのまま記事に遷移する為、何も返さない

# フィードのボックスID更新(ajax)
@ajax_view(login_required=True)
def change_box(request):

    # リクエストパラメータ取得
    try:
        if 'box_id' in request.POST and request.POST['box_id'].isdigit():
            box_id = int(request.POST['box_id'])
        else:
            logger.error('[change_box] box_idが設定されていません。')
            return HttpResponseRedirect(reverse('common_error'))

        if 'feed_id' in request.POST and request.POST['feed_id'].isdigit():
            feed_id = int(request.POST['feed_id'])
        else:
            logger.error('[change_box] feed_idが存在しません。')
            return HttpResponseRedirect(reverse('common_error'))

    except Exception:
        # リクエストパラメータの取得に失敗
        return HttpResponse(simplejson.dumps({
                'result': 'getting param faild.[box_id=' +
                box_id + ',feed_id=' + feed_id + ']'}, ensure_ascii=False),
                mimetype='application/json')

    # フィード更新
    try:
        feed = Feed.objects.filter(id=feed_id, user=request.user)
        feed.box_id = box_id
        feed.save()
    except Exception:
        # フィード更新失敗
        return HttpResponse(simplejson.dumps({'result': 'update feed(box_id) faild.'}, ensure_ascii=False), mimetype='application/json')

    return HttpResponse(simplejson.dumps({'result': 'success', 'feed_id': feed_id}, ensure_ascii=False), mimetype='application/json')

def feed_list(request):

    try:
        manage_kbn = int(request.POST['manage_kbn'])
    except Exception:
        manage_kbn = -1

    #ボックス削除
    if manage_kbn == 1:
        # XXX viewから他のview呼び出し禁止
        del_feed(request)

    # リクエストのボックスID取得
    try:
        box_id = int(request.POST['box_id'])
    except Exception:
        return HttpResponseRedirect(reverse('common_error'))

    if box_id < 0:
        logger.error('[get_feeds] box_idが設定されていません。')
        return HttpResponseRedirect(reverse('common_error'))

    try:
        boxInfo = Box.objects.get(id=box_id)
        boxName = boxInfo.box_name
    except Box.DoesNotExist:
        return HttpResponseRedirect(reverse('common_error'))

    feed_list = Feed.objects.filter(user=request.user,box=boxInfo).order_by('feed_priority', 'id')

    param = {'box_name' : boxName,
             'box_id' : box_id,
             'feed_list' : feed_list}

    return render(request,
                  'feedknot/feed.html',
                  param)
