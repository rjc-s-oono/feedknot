from django.db import models

class Feed(models.Model):
#     box_id = models.ForeignKey()
     box_id = models.IntegerField(u'ボックスID',max_length = 5)
#     user_id = models.ForeignKey()
     user_id = models.IntegerField(u'ユーザID',max_length = 5)
     rss_address = models.URLField(u'RSSアドレス',max_length = 5)
     last_take_date = models.DateTimeField(u'最終読込日時', auto_now_add=False, blank=False, null=False)
     feed_priority= models.IntegerField(u'優先度',max_length = 1)

class Article(models.Model):
#     feed_id = models.ForeignKey()
     feed_id = models.IntegerField(u'フィードID',max_length = 5)
#     box_id = models.ForeignKey()
     box_id = models.IntegerField(u'ボックスID',max_length = 5)
#     user_id = models.ForeignKey()
     user_id = models.IntegerField(u'ユーザID',max_length = 5)
     article_title = models.CharField(u'記事タイトル',max_length = 100)
     article_address = models.URLField(u'記事アドレス')
     pub_date = models.DateTimeField(u'配信日', auto_now_add=False, blank=False, null=False)
     read_flg = models.BooleanField(u'既読フラグ', blank=False, default=False)
