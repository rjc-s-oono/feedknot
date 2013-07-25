# coding: utf-8
import datetime
from django.db import models

from django.contrib.auth.models import User

class Sample(models.Model):
    title = models.CharField(u'タイトル', blank=False, max_length = 100)
    content = models.TextField(u'コメント', blank=True, null=True, max_length = 1000)
    create_by = models.ForeignKey(User, verbose_name=u'作成者', db_column='create_by', related_name='information_create_by')
    updated_by = models.ForeignKey(User, verbose_name=u'最終更新者', db_column='updated_by', related_name='information_updated_by')
    create_date = models.DateTimeField(u'登録日時', auto_now_add=True)
    updated_date = models.DateTimeField(u'更新日時', auto_now=True)
    del_flg = models.BooleanField(u'削除フラグ', blank=False, default=False)

    class Meta:
        db_table = 'sample'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/sample/detail/%i" % self.id

    def add_information(self, request):

        # 現在日時取得
        now = datetime.datetime.now()

        self.create_by = request.user
        self.updated_by = request.user
        self.create_date = now
        self.updated_date = now
        self.del_flg = False
        self.save()

    def edit_information(self, request):

        # 現在日時取得
        now = datetime.datetime.now()

        self.updated_by = request.user
        self.updated_date = now
        self.save()

    def delete_information(self, request):

        # 現在日時取得
        now = datetime.datetime.now()

        self.updated_by = request.user
        self.updated_date = now
        self.del_flg = True
        self.save()
