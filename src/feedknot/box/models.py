# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from feed.models import Feed

class Box(models.Model):
    user = models.ForeignKey(User, verbose_name=u'BOX所有者', db_column='user_id', related_name='box_owner')
    box_name = models.CharField(u'ボックス名', max_length = 255)
    box_priority = models.IntegerField(u'優先度', default = 3)

    class Meta:
        db_table = 'feedknot_box'

    def __unicode__(self):
        return self.box_name

#    def readFeed(self):
#        feed_info_list = Feed.objects.filter(box_id=self.id)
#        for feed_info in feed_info_list:
#            feed_info.readArticle()
