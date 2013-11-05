from django.http import HttpResponse
from django.shortcuts import render_to_response
from feed.models import Article
from time import mktime
from datetime import datetime

import feedparser

def main(request):
    feed_list=[]
    rssurl="http://rss.dailynews.yahoo.co.jp/fc/rss.xml"
    fdp = feedparser.parse(rssurl)
    for entry in fdp['entries']:
        title = entry['title']
        link = entry['link']
        dt = datetime.fromtimestamp(mktime(entry['published_parsed']))
        Article.objects.create(feed_id=0,box_id=1,user_id=2,article_title=title,article_address=link,pub_date=dt)
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

    feed_list = Article.objects.filter(feed_id=0,box_id=1,user_id=2)

    return render_to_response('feedknot/main.html',
                               {'box_title':'ボックスタイトル',
                                'feed_list' : feed_list})