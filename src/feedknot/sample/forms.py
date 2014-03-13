# encoding: UTF-8
from django import forms
from sample.models import Sample

class SampleForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput, required=False, label=u'id')
    title = forms.CharField(label=u'タイトル', widget=forms.TextInput(attrs={'class': 'input'}), max_length=100)
    comment = forms.CharField(label=u'コメント', widget=forms.Textarea(attrs={'class': 'input'}))

    class Meta:
        model = Sample
        exclude = ('create_by','updated_by','create_date','updated_date','del_flg',)
