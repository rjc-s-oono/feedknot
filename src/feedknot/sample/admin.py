# coding: utf-8
from django.contrib import admin

from feed.models import Article
from sample.models import Sample

class SampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')

admin.site.register(Sample, SampleAdmin)
admin.site.register(Article)