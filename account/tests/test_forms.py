# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import account.forms as account_forms

from .base import BaseTest


class UserMinimalRegistrationFormTest(BaseTest):

    def setUp(self):
        super(UserMinimalRegistrationFormTest, self).setUp()


    def test_valid_attempt(self):
        data = {
            "username" : "pdupont",
            "first_name" : "Pierre",
            "last_name" : "Dupont",
            "email" : "pdupont@test.com",
            "password1" : "pdupont_pwd",
            "password2" : "pdupont_pwd",
        }

        form = account_forms.UserMinimalRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_attempt1(self):
        data = {
            "username" : "ab",
            "email" : "aaa",
            "password1" : "p1",
            "password2" : "p2",
        }

        form = account_forms.UserMinimalRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            _("Ensure this value has at least 3 characters (it has 2)."),
            form.errors["username"]
            )
        self.assertIn(
            _("Enter a valid email address."),
            form.errors["email"]
            )
        self.assertIn(
            _("The two password fields didn't match."),
            form.errors["password2"]
            )


    def test_invalid_attempt2(self):
        data = {
            "username" : "jdoe",
            "email" : "jdoe@test.com",
            "password1" : "123",
            "password2" : "123",
        }

        form = account_forms.UserMinimalRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            _("This username already exists. Please try another one."),
            form.errors["username"]
            )
        self.assertIn(
            _("This email address is already used by another user. Please try another one."),
            form.errors["email"]
            )
        self.assertIn(
            _("This password is too short. It must contain at least 8 characters."),
            form.errors["password2"]
            )
        self.assertIn(
            _("This password is entirely numeric."),
            form.errors["password2"]
            )


class CustomLoginFormTest(BaseTest):

    def setUp(self):
        super(CustomLoginFormTest, self).setUp()


    def test_valid_attempt(self):
        data = {
            "username" : "jdoe",
            "password" : "jdoe_pwd"
        }

        form = account_forms.CustomLoginForm(data=data)
        self.assertTrue(form.is_valid())


    def test_invalid_attempt(self):
        data = {
            "username" : "qwerty",
            "password" : "qwertyuiop"
        }

        form = account_forms.CustomLoginForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            _("Please enter a correct username and password. Note that both fields may be case-sensitive."),
            form.non_field_errors()
            )


class UserAccountEditionFormTest(BaseTest):

    def setUp(self):
        super(UserAccountEditionFormTest, self).setUp()
        self.user = User.objects.get(username="jdoe")

    def test_valid_attempt(self):
        data = {
            "first_name" : "Johnny",
            "last_name" : "Doe",
            "email" : "jdoe@test.com",
        }

        form = account_forms.UserAccountEditionForm(self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_attempt(self):
        data = {
            "first_name" : "Johnny",
            "last_name" : "Doe",
            "email" : "fbloggs@test.com",
        }

        form = account_forms.UserAccountEditionForm(self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            _("This email address is already used by another user. Please try another one."),
            form.errors["email"]
            )
