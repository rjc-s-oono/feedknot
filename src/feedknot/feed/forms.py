# -*- coding: utf-8 -*-
from django import forms

class AddFeedForm(forms.Form):

    url = forms.URLField(max_length = 255)
    title = forms.CharField(max_length=100)
    className = forms.CharField()

class DeleteFeedForm(forms.Form):

    feed_id = forms.IntegerField(min_value=1, max_value=99999999999)

class MarkReadArticleForm(forms.Form):

    box_id = forms.IntegerField(min_value=1, max_value=99999999999)
    feed_id = forms.IntegerField(min_value=1, max_value=99999999999)
    article_id = forms.IntegerField(min_value=1, max_value=99999999999)