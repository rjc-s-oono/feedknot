from django.http import HttpResponse
from django.shortcuts import render_to_response
from feed.models import Article
from feed.models import Feed
from time import mktime
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

import feedparser

def main(request):

    try:
        feedInfo = Feed.objects.get(id=1,box_id=1,user_id=1)
    except ObjectDoesNotExist:
        Feed.objects.create(box_id=1,user_id=1,rss_address="http://rss.dailynews.yahoo.co.jp/fc/rss.xml",last_take_date=datetime.today(),feed_priority=1)
        feedInfo = Feed.objects.get(id=1,box_id=1,user_id=1)
    rssurl= feedInfo.rss_address
    ltd = feedInfo.last_take_date
    tz = ltd.tzinfo
    feedInfo.last_take_date = datetime.today()


    article_list=[]

    fdp = feedparser.parse(rssurl)
    for entry in fdp['entries']:
        title = entry['title']
        link = entry['link']
        dt = datetime.fromtimestamp(mktime(entry['published_parsed']), tz)
        if ltd < dt:
            Article.objects.create(feed_id=1,box_id=1,user_id=1,article_title=title,article_address=link,pub_date=dt)
        #feed={'feedId':'1234',
        #       'url':link,
        #       'articleSubject':title,
        #       'articleDate':'2013/12/12 12:12',
        #       'articleSiteName':'サイト名'}
        #feed_list.append(feed)


  #  feed={'feedId':'9876',
  #         'url':'666666',
  #         'articleSubject':'Subject2',
  #         'articleContent':'Content2',
  #         'articleDate':'2013/12/12 12:10',
  #         'articleSiteName':'サイト名2'}
  #  feed_list.append(feed)

    feedInfo.save();

    article_list = Article.objects.filter(feed_id=1,box_id=1,user_id=1)

    return render_to_response('feedknot/main.html',
                               {'box_title':'ボックスタイトル',
                                'article_list' : article_list})