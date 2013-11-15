from django.db import models

class LoginMaster(models.Model):
    google_id = models.CharField(u'Google メールアドレス', max_length = 127, blank = True)
    facebook_id = models.CharField(u'Facebook メールアドレス', max_length = 127, blank = True)
    twitter_id = models.CharField(u'Twitter アカウント', max_length = 127, blank = True)
    mail_address = models.EmailField(u'メールアドレス')
    default_box_id = models.IntegerField(u'ボックスID', max_length = 5)
    #default_box_id = models.ForeignKey(Box,null=True)

    def __unicode__(self):
        return self.mail_address
