# -*- coding: utf-8 -*-
import logging
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils import simplejson

from common.decorators import ajax_view
#from common.utils import datetime_util

from administration.models import LoginMaster
from box.models import Box
from feed.models import Article, Feed

from feed.forms import AddFeedForm, DeleteFeedForm, MarkReadArticleForm

logger = logging.getLogger('application')

@login_required
def main(request):

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

@login_required
def main_select_box(request, box_id):

    user = request.user
    logger.debug("user_id: %s" % (user.id))

    try:
        box_info = Box.objects.get(pk=box_id, user=user, del_flg=False)
        box_name = box_info.box_name
        box_info.read_feed()
    except Box.DoesNotExist:
        raise Http404

    box_list = Box.objects.filter(user=user, del_flg=False).order_by('box_priority')

    article_list = Article.objects.filter(box=box_info, user=user, del_flg=False).order_by('-pub_date', 'pk')

    param = {'box_name' : box_name,
             'article_list' : article_list,
             'box_list' : box_list}

    return render(request,
                  'feedknot/main.html',
                  param)


@login_required
def feed_list(request, box_id):

    # ボックス取得
    try:
        box_info = Box.objects.get(id=box_id, user=request.user, del_flg=False)
        box_name = box_info.box_name
    except Box.DoesNotExist:
        logger.error('[feed_list] box_idが不正です。')
        raise Http404

    feed_list = Feed.objects.filter(box=box_info, user=request.user, del_flg=False).order_by('feed_priority', 'id')

    param = {'box_name' : box_name,
             'box_id' : box_id,
             'feed_list' : feed_list,
             'feed_priority': [3, 2, 1]}

    return render(request,
                  'feedknot/feed.html',
                  param)

@login_required
def search_feed(request, box_id):

    try:
        box = Box.objects.get(id=box_id, user=request.user, del_flg=False)
    except Box.DoesNotExist:
        raise Http404

    return render(request,
                  'feedknot/search_feed.html',
                  {'box_id':box.id})

# フィード追加(ajax)
@ajax_view(FormClass=AddFeedForm ,login_required=True)
def add_feed(request, box_id):

    add_feed_form = AddFeedForm(request.POST)
    add_feed_form.is_valid()

    rss_address = add_feed_form.cleaned_data['url']
    title = add_feed_form.cleaned_data['title']
    class_name = add_feed_form.cleaned_data['className']

    try:
        # ボックス取得
        box = Box.objects.get(id=box_id, user=request.user, del_flg=False)

        # 最初は2000年1月1日からのフィードを全て取得する
        today = datetime.date(2000, 1, 1)


        existChk = Feed.objects.filter(rss_address=rss_address, user=request.user, del_flg=False)

        if len(existChk) != 0:
            result = {'result': 'error2',
                      'message': 'addNG'}

            return HttpResponse(simplejson.dumps(result, ensure_ascii=False), mimetype='application/json')

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

# XXX 関数の挙動がわからないので要確認
@login_required
def get_feeds(request, box_id):

    defBoxExistFlg = True
    # デフォルトボックスID取得
    if box_id < 0:
        try:
            login_info = LoginMaster.objects.get(user=request.user, del_flg=False)
            default_box = login_info.default_box
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
            box_info = Box.objects.get(id=box_id, del_flg=False)
            box_name = box_info.box_name
            box_info.read_feed()
        except Box.DoesNotExist:
            defBoxExistFlg = False

    if (not defBoxExistFlg):
        box_name = "ボックスが登録されていません。"

    feed_list = Feed.objects.filter(box=box_info, user=request.user, del_flg=False).order_by('priority', 'id')

    param = {'box_name' : box_name,
         'feed_list' : feed_list}

    return render(request,
                  'feedknot/main.html',
                  param)

# FIXME 使用箇所不明
# フィードのボックスID更新(ajax)
@ajax_view(login_required=True)
def change_box(request, box_id):

    # リクエストパラメータ取得
    try:
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
        feed = Feed.objects.filter(id=feed_id, user=request.user, del_flg=False)
        feed.box_id = box_id
        feed.save()
        # XXX 記事もbox_idを持っているので、データ不整合が発生する
    except Exception:
        # フィード更新失敗
        return HttpResponse(simplejson.dumps({'result': 'update feed(box_id) faild.'}, ensure_ascii=False), mimetype='application/json')

    return HttpResponse(simplejson.dumps({'result': 'success', 'feed_id': feed_id}, ensure_ascii=False), mimetype='application/json')


# フィード削除(ajax)
@ajax_view(FormClass=DeleteFeedForm ,login_required=True)
def del_feed(request, box_id):

    delete_feed_form = DeleteFeedForm(request.POST)
    delete_feed_form.is_valid()

    feed_id = delete_feed_form.cleaned_data['feed_id']

    # フィード削除
    try:
        box = Box.objects.get(id=box_id, user=request.user)
        Feed.objects.filter(id=feed_id, box=box, user=request.user).delete()

        feed_list = Feed.objects.filter(box=box, user=request.user, del_flg=False)

        result = {'result': 'success', 'feed_list': [feed.as_json() for feed in feed_list], 'feed_priority': [3, 2, 1]}
    except Box.DoesNotExist:
        result = {'result': 'error',
                  'message': 'Box does not exist.[box_id=' + str(box_id) + ']'}
    except Exception:
        # フィードの削除失敗
        result = {'result': 'error',
                  'message': 'delete feed faild.[box_id=' + str(box_id) + ',feed_id=' + str(feed_id) + ']'}

    logger.debug(result)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), mimetype='application/json')

# 記事既読更新(ajax)
@ajax_view(FormClass=MarkReadArticleForm ,login_required=True)
def upd_article(request):

    mark_read_article_form = MarkReadArticleForm(request.POST)
    mark_read_article_form.is_valid()

    article_id = mark_read_article_form.cleaned_data['article_id']

    # 記事更新
    try:
        article = Article.objects.get(id=article_id, user=request.user, del_flg=False)
        article.mark_read_article()

        result = {'result': 'success'}
    except Article.DoesNotExist:
        result = {'result': 'error',
                  'message': 'Article does not exist.[article_id=' + str(article_id) + ']'}
    except Exception:
        # 記事更新失敗
        result = {'result': 'error',
                  'message': 'update article faild.'}

    logger.debug(result)
    return HttpResponse(simplejson.dumps(result, ensure_ascii=False), mimetype='application/json')
