# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from box.models import Box

class LoginMaster(models.Model):
    user = models.ForeignKey(User, verbose_name=u'ユーザ', db_column='user_id', related_name='loginmaster_user', unique=True)
    default_box = models.ForeignKey(Box, verbose_name=u'デフォルトボックスID', db_column='default_box_id', related_name='loginmaster_default_box_id', blank=True, null=True)
    create_date = models.DateTimeField(u'登録日時', auto_now_add=True)
    updated_date = models.DateTimeField(u'更新日時', auto_now=True)
    del_flg = models.BooleanField(u'削除フラグ', blank=False, default=False)

    class Meta:
        db_table = 'feedknot_login_master'

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.default_box_id)

    def set_default_box(self, request):

        # 現在日時取得
        now = datetime.datetime.now()

        box = Box()
        box.box_name = "デフォルトボックス"
        box.user = request.user
        box.add_box()

        self.user = request.user
        self.default_box = box
        self.create_date = now
        self.updated_date = now
        self.del_flg = False
        self.save()

    def edit_default_box(self, request):
        self.save()

