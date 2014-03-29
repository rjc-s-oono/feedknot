# encoding: UTF-8
'''
Created on 2013/06/30

@author: toshiya.sugano
'''
import math
from django import template

register = template.Library()

@register.filter(name='sub')
def subtracts(value, arg):
    "Subtracts the arg from the value"
    return int(value) - int(arg)

@register.filter(name='mult')
def multiplies(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)

@register.filter(name='div')
def divides(value, arg):
    "Divides the value by the arg"
    return int(value) / int(arg)

@register.filter(name='mod')
def modulo(value, arg):
    "Modulo the value by the arg"
    return int(value) % int(arg)

@register.filter(name='abs')
def absolute(value):
    "Absolute the value by the arg"
    return math.fabs(value)