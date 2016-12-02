# -*- coding: utf-8 -*-

import logging
LOGGER = logging.getLogger(__name__)

from django.apps import AppConfig
from django.conf import settings
from django.urls import reverse

class AccountConfig(AppConfig):
    name = 'account'
    verbose_name = "account"

    def chek_settings(self):
        expected_login_url_setting = reverse("account:login")
        if getattr(settings, "LOGIN_URL", None) != expected_login_url_setting:
            LOGGER.warning(
                "The integration of the 'Account' application requires the " \
                "definition of the LOGIN_URL, LOGIN_REDIRECT_URL and " \
                "LOGOUT_REDIRECT_URL parameters in you project settings file. " \
                "Especially the LOGIN_URL which should be set as " \
                "LOGIN_URL=%s' to play smoothly with this app." \
                % expected_login_url_setting
                )

    def ready(self):
        self.chek_settings()
