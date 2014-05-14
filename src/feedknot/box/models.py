# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

class Box(models.Model):
    user = models.ForeignKey(User, verbose_name=u'BOX所有者', db_column='user_id', related_name='box_owner')
    box_name = models.CharField(u'ボックス名', max_length = 255)
    box_priority = models.IntegerField(u'優先度', default = 3)
    create_date = models.DateTimeField(u'登録日時', auto_now_add=True)
    updated_date = models.DateTimeField(u'更新日時', auto_now=True)
    del_flg = models.BooleanField(u'削除フラグ', blank=False, default=False)

    class Meta:
        db_table = 'feedknot_box'

    def __unicode__(self):
        return self.box_name

    def as_json(self):
        return dict(
            id=self.id,
            user=dict(
                      id=self.user.id
                      ),
            box_name=self.box_name,
            box_priority=self.box_priority,
            feed_list_url=reverse('feed_list', args=[self.id]),
            )

    def add_box(self):
        # 現在日時取得
        now = datetime.datetime.now()

        self.create_date = now
        self.updated_date = now
        self.del_flg = False
        self.save()

    def read_feed(self):
        feed_info_list = self.feed_box.all()
        for feed_info in feed_info_list:
            feed_info.readArticle()

    def edit_box_name(self, box_name):
        # 現在日時取得
        now = datetime.datetime.now()

        self.box_name = box_name
        self.updated_date = now
        self.save()

    def edit_box_priority(self, box_priority):
        # 現在日時取得
        now = datetime.datetime.now()

        self.box_priority = box_priority
        self.updated_date = now
        self.save()
