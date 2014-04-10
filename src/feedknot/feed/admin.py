# -*- coding: utf-8 -*-
from django.contrib import admin


from feed.models import Article
from feed.models import Feed

admin.site.register(Article)
admin.site.register(Feed)