# -*- coding: utf-8 -*-

import logging
LOGGER = logging.getLogger(__name__)

from django.shortcuts import render

from django.utils.translation import ugettext_lazy as _

def homepage(request):
    return render(request, 'homepage/homepage.html')
