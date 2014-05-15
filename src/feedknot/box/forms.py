# -*- coding: utf-8 -*-
from django import forms

class EditDefaultBoxForm(forms.Form):

    box_id = forms.IntegerField(min_value=1, max_value=99999999999)

class EditBoxNameForm(forms.Form):

    box_id = forms.IntegerField(min_value=1, max_value=99999999999)
    box_name = forms.CharField(max_length=255)

class EditBoxPriorityForm(forms.Form):

    box_id = forms.IntegerField(min_value=1, max_value=99999999999)
    box_priority = forms.IntegerField(min_value=1, max_value=3)

class DeleteBoxForm(forms.Form):

    box_id = forms.IntegerField(min_value=1, max_value=99999999999)