# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from box.models import Box
from feed.models import Article
from feed.models import Feed

class LoginMaster(models.Model):
    user = models.ForeignKey(User, unique=True)
    default_box_id = models.IntegerField(u'デフォルトボックスID', max_length = 5)
    #default_box_id = models.ForeignKey(Box,null=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.user.id

    def del_box(self, box_id):
        Article.objects.filter(box_id=box_id, user_id=self.id).delete()
        Feed.objects.filter(box_id=box_id, user_id=self.id).delete()
        Box.objects.filter(id=box_id, user_id=self.id).delete()
