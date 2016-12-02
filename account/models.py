# -*- coding: utf-8 -*-

import logging
LOGGER = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserProfile(models.Model):
    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return _("%s's profile") % self.user.username


class Address(models.Model):
    class Meta:
        verbose_name = _("adress")
        verbose_name_plural = _("adresses")

    street_1 = models.CharField(
        max_length=100,
        blank=True,
        default="",
        )

    street_2 = models.CharField(
        max_length=100,
        blank=True,
        default=""
        )

    city = models.CharField(
        max_length=100,
        blank=True,
        default=""
        )

    zipcode = models.CharField(
        max_length=100,
        blank=True,
        default=""
        )

    country = models.CharField(
        max_length=100,
        blank=True,
        default=""
        )

    userprofile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        null=True
        )

    def __str__(self):
        return _("%s's address") % self.userprofile.user.username
