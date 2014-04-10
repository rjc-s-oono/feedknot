# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
import feedparser
from time import mktime

class Feed(models.Model):
#     box_id = models.ForeignKey()
    box_id = models.IntegerField(u'ボックスID',max_length = 5)
#     user_id = models.ForeignKey()
    user_id = models.IntegerField(u'ユーザID',max_length = 5)
    rss_address = models.URLField(u'RSSアドレス',max_length = 255)
    last_take_date = models.DateTimeField(u'最終読込日時', auto_now_add=False, blank=False, null=False)
    feed_priority= models.IntegerField(u'優先度',max_length = 1)

    def readArticle(self):
        rssurl= self.rss_address
        ltd = self.last_take_date
        tz = ltd.tzinfo
        fdp = feedparser.parse(rssurl)
        stitle = fdp.feed.title
        for entry in fdp['entries']:
            try:
                title = entry['title']
            except KeyError:
                title = "タイトルなし"

            try:
                link = entry['link']
            except KeyError:
                link = "about:blank"

            #要相談 日本時間の設定方法、rdfの読み込み（published_parsed取得でエラー）
            try:
                dt = datetime.fromtimestamp(mktime(entry['published_parsed']) + 32400, tz)
            except KeyError:
                try:
                    dt = datetime.fromtimestamp(mktime(entry['updated_parsed']) + 32400, tz)
                except KeyError:
                    continue

            if ltd < dt:
                Article.objects.create(feed_id=self.id ,box_id=self.box_id ,user_id=self.user_id ,site_title=stitle,article_title=title,article_address=link,pub_date=dt)

            if self.last_take_date < dt:
                self.last_take_date = dt
        self.save();

class Article(models.Model):
#     feed_id = models.ForeignKey()
    feed_id = models.IntegerField(u'フィードID',max_length = 5)
#     box_id = models.ForeignKey()
    box_id = models.IntegerField(u'ボックスID',max_length = 5)
#     user_id = models.ForeignKey()
    user_id = models.IntegerField(u'ユーザID',max_length = 5)
    site_title = models.CharField(u'サイトタイトル',max_length = 100)
    article_title = models.CharField(u'記事タイトル',max_length = 100)
    article_address = models.URLField(u'記事アドレス')
    pub_date = models.DateTimeField(u'配信日', auto_now_add=False, blank=False, null=False)
    read_flg = models.BooleanField(u'既読フラグ', blank=False, default=False)
