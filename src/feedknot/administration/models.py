# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from box.models import Box

class LoginMaster(models.Model):
    user = models.ForeignKey(User, verbose_name=u'ユーザ', db_column='user_id', related_name='loginmaster_user', unique=True)
    default_box_id = models.ForeignKey(Box, verbose_name=u'デフォルトボックスID', db_column='default_box_id', related_name='loginmaster_default_box_id', blank=True, null=True)

    class Meta:
        db_table = 'feedknot_login_master'

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.default_box_id)
