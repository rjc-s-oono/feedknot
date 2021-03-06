# -*- coding: utf-8 -*-
import logging
import feedparser
from time import mktime
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from box.models import Box

logger = logging.getLogger('application')

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

    def as_json(self):
        return dict(
            id=self.id,
            box=dict(
                     id=self.box.id
                     ),
            user=dict(
                      id=self.user.id
                      ),
            feed_name=self.feed_name,
            rss_address=self.rss_address,
            last_take_date=self.last_take_date.strftime("%Y/%m/%d %H:%M:%S"),
            feed_priority=self.feed_priority,
            )

    def add_feed(self):
        # 現在日時取得
        now = datetime.now()

        # フィードを取得
        fdp = feedparser.parse(self.rss_address)

        self.feed_name = fdp.feed.title
        self.create_date = now
        self.updated_date = now
        self.del_flg = False
        self.save()

    def read_article(self):
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

            logger.debug("last_take_date: %s, published_parsed: %s" % (ltd, dt));

            if ltd < dt:
                try:
                    article = Article.objects.get(feed_id=self.id, box_id=self.box_id ,user_id=self.user_id, article_address=link, del_flg=False)
                    article.article_title = title
                    article.pub_date = dt
                    article.edit_article()
                except Article.DoesNotExist:
                    # 記事アドレスが同じ既存データがない場合は、記事を新規作成
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

    def as_json(self):
        return dict(
            id=self.id,
            feed=dict(
                      id=self.feed.id
                      ),
            box=dict(
                     id=self.box.id
                     ),
            user=dict(
                      id=self.user.id
                      ),
            site_title=self.site_title,
            article_title=self.article_title,
            article_address=self.article_address,
            pub_date=self.pub_date.strftime("%Y/%m/%d %H:%M:%S"),
            read_flg=self.read_flg,
            )

    def mark_read_article(self):
        # 現在日時取得
        now = datetime.now()

        self.read_flg = True
        self.updated_date = now
        self.save()

    def edit_article(self):
        # 現在日時取得
        now = datetime.now()

        self.updated_date = now
        self.save()
