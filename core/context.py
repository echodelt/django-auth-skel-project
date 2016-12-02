# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import reverse

def site_context(request):
    context = {

        'brand_name': settings.BRAND_NAME,
        'site_title': settings.SITE_TITLE,

        'homepage_url': reverse('homepage'),
        'account_login_url': reverse('account:login'),
        'account_register_url': reverse('account:register'),
        'account_view_profile_url': reverse('account:view-profile'),
        'account_edit_profile_url': reverse('account:edit-profile'),
        'account_password_change_url': reverse('account:password-change'),

    }
    return context
