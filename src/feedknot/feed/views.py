from django.shortcuts import render_to_response
from box.models import Box
from feed.models import Article
from feed.models import Feed
from django.core.exceptions import ObjectDoesNotExist

def main(request):

    boxName = ""
    try:
        boxInfo = Box.objects.get(id=1)
        boxName = boxInfo.box_name
        boxInfo.readFeed()
    except ObjectDoesNotExist:
        boxName = "NoName"

    article_list = Article.objects.filter(box_id=1).order_by('-pub_date')
    box_list = Box.objects.filter(user_id=1).order_by('box_priority')

    return render_to_response('feedknot/main.html',
                               {'box_name' : boxName,
                                'article_list' : article_list,
                                'box_list' : box_list})

