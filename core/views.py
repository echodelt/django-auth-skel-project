# -*- coding: utf-8 -*-

import logging
LOGGER = logging.getLogger(__name__)

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


def custom_handler404(request):
    return render(request, '404.html')


def custom_handler500(request):
    return render(request, '500.html')
