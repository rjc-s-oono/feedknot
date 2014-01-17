from django.shortcuts import render_to_response
from box.models import Box
from feed.models import Article
from feed.models import Feed
from administration.models import LoginMaster
from django.core.exceptions import ObjectDoesNotExist

def main(request,user_id,box_id):

    try:
        user_id = int(user_id)
    except Exception:
        user_id = -1
    try:
        box_id = int(box_id)
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

    article_list = Article.objects.filter(box_id=box_id).order_by('-pub_date')
    box_list = Box.objects.filter(user_id=user_id).order_by('box_priority')

    return render_to_response('feedknot/main.html',
                               {'user_id' : user_id,
                                'box_name' : boxName,
                                'article_list' : article_list,
                                'box_list' : box_list})

