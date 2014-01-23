from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from box.models import Box
from feed.models import Article
from feed.models import Feed
from administration.models import LoginMaster
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

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

    article_list = Article.objects.filter(box_id=box_id).order_by('-pub_date')
    box_list = Box.objects.filter(user_id=user_id).order_by('box_priority')

    param = {'user_id' : user_id,
         'box_name' : boxName,
         'article_list' : article_list,
         'box_list' : box_list}
    param.update(csrf(request))

    return render_to_response('feedknot/main.html',
                               param)

