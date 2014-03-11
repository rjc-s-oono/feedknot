from django.db import models
from django.contrib.auth.models import User

class LoginMaster(models.Model):
    user = models.ForeignKey(User, unique=True)
    default_box_id = models.IntegerField(u'デフォルトボックスID', max_length = 5)
    #default_box_id = models.ForeignKey(Box,null=True)

    class Meta:
        pass

    def __unicode__(self):
        return self.user.id
