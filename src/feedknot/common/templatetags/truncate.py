# encoding: UTF-8
'''
Created on 2013/06/30

@author: toshiya.sugano
'''
from django import template

register = template.Library()

# 文字列をarg文字以内に切り詰める。超えた場合は末尾を'…'にする。
@register.filter(name='truncate')
def truncate(value, arg):
    value = value.strip()
    if len(value) <= arg:
        return value
    arg -= 1
    return value[:arg].strip() + u"…"