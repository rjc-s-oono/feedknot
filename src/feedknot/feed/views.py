from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from box.models import Box
from feed.models import Article
from feed.models import Feed
from administration.models import LoginMaster
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import json
from django.http.response import HttpResponse

def main(request):

    user_id = 1
    box_id = -1
    if request.user.is_authenticated():
        user_id=request.user.id

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
            boxName = "NoName"
    else:
        try:
            loginInfo = LoginMaster.objects.get(id=user_id)
            box_id = loginInfo.default_box_id
            boxInfo = Box.objects.get(id=box_id)
            boxName = boxInfo.box_name
            boxInfo.readFeed()
        except ObjectDoesNotExist:
            boxName = "NoName"

    article_list = Article.objects.filter(box_id=box_id).order_by('-pub_date', 'id')
    box_list = Box.objects.filter(user_id=user_id).order_by('box_priority')

    param = {'user_id' : user_id,
         'box_name' : boxName,
         'article_list' : article_list,
         'box_list' : box_list}
    param.update(csrf(request))

    return render_to_response('feedknot/main.html',
                               param)

# 返却値(失敗)
RESPONSE_ERR = HttpResponse(json.dumps({'result': 'err'}), mimetype='application/json')

# フィード追加(ajax)
def add_feed(request):
    box_id = -1
    user_id = 1
    rssaddress = ''
    title = ''
    
    if not request.is_ajax():
        return RESPONSE_ERR
    
    # ユーザID取得
    if request.user.is_authenticated():
        user_id=request.user.id
    else:
        user_id=1
    
    try:
        rssaddress = request.POST.is_valid()
    except Exception:
        return HttpResponse(json.dumps({'result': '[1]koko?'}), mimetype='application/json')
    
    # ボックスID取得
    try:
        box_id = int(request.POST['box_id'])
        rssaddress = request.POST['url']
        title = request.POST['title']
    except Exception:
        return RESPONSE_ERR
    
    # フィード登録
    feed = Feed(box_id=box_id, user_id=user_id,
                rss_address=rssaddress,feed_priority=3)
    feed.save()
    
    res = json.dumps({'result': 'success', 'title': title})
    #res.update(csrf(request))
    
    return HttpResponse(json.dumps(res), mimetype='application/json')

