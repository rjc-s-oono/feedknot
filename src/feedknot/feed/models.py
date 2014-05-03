# -*- coding: utf-8 -*-
import feedparser
from time import mktime
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from box.models import Box

class Feed(models.Model):
    box = models.ForeignKey(Box, verbose_name=u'ボックスID', db_column='box_id', related_name='feed_box')
    user = models.ForeignKey(User, verbose_name=u'フィード所有者', db_column='user_id', related_name='feed_owner')
    feed_name = models.CharField(u'サイトタイトル',max_length = 100)
    rss_address = models.URLField(u'RSSアドレス', max_length = 255)
    last_take_date = models.DateTimeField(u'最終読込日時', auto_now_add=False, blank=False, null=False)
    feed_priority= models.IntegerField(u'優先度', max_length = 1)
    create_date = models.DateTimeField(u'登録日時', auto_now_add=True)
    updated_date = models.DateTimeField(u'更新日時', auto_now=True)
    del_flg = models.BooleanField(u'削除フラグ', blank=False, default=False)

    class Meta:
        db_table = 'feedknot_feed'

    def __unicode__(self):
        return self.feed_name

    def add_feed(self):

        # 現在日時取得
        now = datetime.now()

        self.create_date = now
        self.updated_date = now
        self.del_flg = False
        self.save()

    def readArticle(self):
        rssurl= self.rss_address
        ltd = self.last_take_date
        tz = ltd.tzinfo
        fdp = feedparser.parse(rssurl)
        try:
            stitle = fdp.feed.title
        except Exception:
            return

        for entry in fdp['entries']:

            title = entry.get('title', '')
            if title == '':
                title = "タイトルなし"

            link = entry.get('link', '')
            if link == '':
                link = "about:blank"

            #暫定処理 updated_parsedが非推奨のためfeedparserをバージョンアップするとエラーとなる可能性がある
            published_parsed = entry.get('published_parsed', '')

            if published_parsed == '':
                published_parsed = entry.get('updated_parsed', '')

            if published_parsed == '':
                continue

            dt = datetime.fromtimestamp(mktime(published_parsed) + 32400, tz)

            if ltd < dt:
                Article.objects.create(feed_id=self.id ,box_id=self.box_id ,user_id=self.user_id ,site_title=stitle,article_title=title,article_address=link,pub_date=dt)

            if self.last_take_date < dt:
                self.last_take_date = dt
        self.save();

class Article(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=u'フィードID', db_column='feed_id', related_name='article_feed')
    box = models.ForeignKey(Box, verbose_name=u'ボックスID', db_column='box_id', related_name='article_box')
    user = models.ForeignKey(User, verbose_name=u'記事所有者', db_column='user_id', related_name='article_owner')
    site_title = models.CharField(u'サイトタイトル', max_length=100)
    article_title = models.CharField(u'記事タイトル', max_length=100)
    article_address = models.URLField(u'記事アドレス' , max_length=255)
    pub_date = models.DateTimeField(u'配信日', auto_now_add=False, blank=False, null=False)
    read_flg = models.BooleanField(u'既読フラグ', blank=False, default=False)
    create_date = models.DateTimeField(u'登録日時', auto_now_add=True)
    updated_date = models.DateTimeField(u'更新日時', auto_now=True)
    del_flg = models.BooleanField(u'削除フラグ', blank=False, default=False)

    class Meta:
        db_table = 'feedknot_article'

    def __unicode__(self):
        return "%s - %s" % (self.site_title, self.article_title)
