from django.db import models

class Box(models.Model):
    user_id = models.IntegerField(u'ユーザID', max_length = 5)
    #user_id = models.ForeignKey(User)
    box_name = models.CharField(u'ボックス名', max_length = 255)
    # とりあえず5段階で真ん中のイメージ
    box_priority = models.IntegerField(u'優先度', default = 3)

    def __unicode__(self):
        return self.box_name
