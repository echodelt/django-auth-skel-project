# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter(name='iternum')
def iternum(args):
    # args : a string like "1,5"
    arg_list = [arg.strip() for arg in args.split(',')]
    return range(int(arg_list[0]), int(arg_list[1]) + 1)
