# -*- coding: utf-8 -*-
from django import forms

class AddFeedForm(forms.Form):

    box_id = forms.IntegerField(min_value=1, max_value=99999999999)
    url = forms.URLField(max_length = 255)
    title = forms.CharField(max_length=100)
    className = forms.CharField()