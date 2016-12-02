# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import account.forms as account_forms

from .base import BaseTest


class AnonymousUserViewTest(BaseTest):

    def setUp(self):
        super(AnonymousUserViewTest, self).setUp()


    def check_get_request_status_code(
        self,
        path,
        expected_status_code
        ):
        response = self.client.get(
            path=path,
            follow=False
        )
        self.assertEqual(response.status_code, expected_status_code)


    def test_get_home_status_code(self):
        self.check_get_request_status_code(
            reverse("account:home"),
            302
            )


    def test_get_register_status_code(self):
        self.check_get_request_status_code(
            reverse("account:register"),
            200
            )


    def test_get_register_confirm_status_code(self):
        self.check_get_request_status_code(
            reverse("account:register-confirm"),
            200
            )


    def test_get_login_status_code(self):
        self.check_get_request_status_code(
            reverse("account:login"),
            200
            )


    def test_get_logout_status_code(self):
        self.check_get_request_status_code(
            reverse("account:logout"),
            302
            )


    def test_get_view_profile_status_code(self):
        self.check_get_request_status_code(
            reverse("account:view-profile"),
            302
            )


    def test_get_edit_profile_status_code(self):
        self.check_get_request_status_code(
            reverse("account:edit-profile"),
            302
            )


    def test_get_password_change_status_code(self):
        self.check_get_request_status_code(
            reverse("account:password-change"),
            302
            )


    def test_get_password_change_done_status_code(self):
        self.check_get_request_status_code(
            reverse("account:password-change-done"),
            302
            )


    def test_get_password_reset_status_code(self):
        self.check_get_request_status_code(
            reverse("account:password-reset"),
            200
            )


    def test_get_password_reset_done_status_code(self):
        self.check_get_request_status_code(
            reverse("account:password-reset-done"),
            200
            )


    def test_get_reset_complete_status_code(self):
        self.check_get_request_status_code(
            reverse("account:password-reset-complete"),
            200
            )


    def check_get_request_redirection(
        self,
        path,
        expected_redirection_path
        ):
        response = self.client.get(
            path=path,
            follow=True
        )
        self.assertEqual(
            response.redirect_chain[-1][0],
            expected_redirection_path
            )


    def test_get_home_redirection(self):
        self.check_get_request_redirection(
            reverse("account:home"),
            "%s?next=%s" % (settings.LOGIN_URL, reverse("account:home"))
            )


    def test_get_logout_redirection(self):
        self.check_get_request_redirection(
            reverse("account:logout"),
            settings.LOGOUT_REDIRECT_URL
            )


    def test_get_view_profile_redirection(self):
        self.check_get_request_redirection(
            reverse("account:view-profile"),
            "%s?next=%s" % (settings.LOGIN_URL, reverse("account:view-profile"))
            )


    def test_get_edit_profile_redirection(self):
        self.check_get_request_redirection(
            reverse("account:edit-profile"),
            "%s?next=%s" % (settings.LOGIN_URL, reverse("account:edit-profile"))
            )


    def test_get_password_change_redirection(self):
        self.check_get_request_redirection(
            reverse("account:password-change"),
            "%s?next=%s" % (settings.LOGIN_URL, reverse("account:password-change"))
            )


    def test_register_valid_attempt(self):
        data = {
            "username" : "pdupont",
            "first_name" : "Pierre",
            "last_name" : "Dupont",
            "email" : "pdupont@test.com",
            "password1" : "pdupont_pwd",
            "password2" : "pdupont_pwd",
        }
        response = self.client.post(
            path=reverse("account:register"),
            data=data,
            follow=True
        )

        self.assertEqual(
            response.redirect_chain[-1][0],
            reverse("account:register-confirm")
            )
        user = User.objects.get(username="pdupont")
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name,  data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertTrue(user.check_password(data["password1"]))


    def test_register_invalid_attempt1(self):
        data = {
            "username" : "ab",
            "email" : "aaa",
            "password1" : "p1",
            "password2" : "p2",
        }
        response = self.client.post(
            path=reverse("account:register"),
            data=data,
            follow=True
        )

        self.assertFormError(
            response,
            "form",
            "username",
             _("Ensure this value has at least 3 characters (it has 2).")
            )
        self.assertFormError(
            response,
            "form",
            "email",
             _("Enter a valid email address.")
            )
        self.assertFormError(
            response,
            "form",
            "password2",
             _("The two password fields didn't match.")
            )


    def test_register_invalid_attempt2(self):
        data = {
            "username" : "jdoe",
            "email" : "jdoe@test.com",
            "password1" : "123",
            "password2" : "123",
        }
        response = self.client.post(
            path=reverse("account:register"),
            data=data,
            follow=True
        )

        self.assertFormError(
            response,
            "form",
            "username",
             _("This username already exists. Please try another one.")
            )
        self.assertFormError(
            response,
            "form",
            "email",
             _("This email address is already used by another user. Please try another one.")
            )
        expected_password2_errors = [
            _("This password is too short. It must contain at least 8 characters."),
            _("This password is entirely numeric.")
        ]
        self.assertFormError(
            response,
            "form",
            "password2",
             expected_password2_errors
            )


    def test_login_as_registered_user(self):
        data = {
            "username" : "jdoe",
            "password" : "jdoe_pwd"
        }
        response = self.client.post(
            path=reverse("account:login"),
            data=data,
            follow=True
        )

        self.assertEqual(
            response.redirect_chain[-1][0],
            settings.LOGIN_REDIRECT_URL
            )
        self.assertIn("_auth_user_id", self.client.session)
        self.assertEqual(self.client.session["_auth_user_id"], "1")
        self.assertEqual(
            response.context["user"].username,
            "jdoe"
            )
        self.assertEqual(
            response.context["user"].first_name,
            "John"
            )
        self.assertEqual(
            response.context["user"].last_name,
            "Doe"
            )
        self.assertEqual(
            response.context["user"].email,
            "jdoe@test.com"
            )


    def test_login_as_unregistered_user(self):
        data = {
            "username" : "qwerty",
            "password" : "qwertyuiop"
        }
        response = self.client.post(
            path=reverse("account:login"),
            data= data,
            follow=True
        )

        self.assertFalse(response.context["form"].is_valid())
        self.assertFormError(
            response,
            "form",
            None,
             _("Please enter a correct username and password. Note that both fields may be case-sensitive.")
            )
        self.assertNotIn("_auth_user_id", self.client.session)


class LoggedUserViewTest(BaseTest):

    def setUp(self):
        super(LoggedUserViewTest, self).setUp()

        data = {
            "username" : "jdoe",
            "password" : "jdoe_pwd"
        }
        response = self.client.post(
            path=reverse("account:login"),
            data = data,
            follow=True
        )

        self.assertEqual(
            response.context["user"].username,
            "jdoe"
            )


    def test_edit_profile_valid_attempt(self):
        data = {
            "first_name" : "Johnny",
            "last_name" : "Doe",
            "email" : "jdoe@test.com",
            "street_1" : "76 Old Chapel Road",
            "street_2" : "",
            "city" : "GARVESTONE",
            "zipcode" : "NR9 0HQ",
            "country" : "UK"
        }
        response = self.client.post(
            path=reverse("account:edit-profile"),
            data=data,
            follow=True
        )

        self.assertEqual(
            response.redirect_chain[-1][0],
            reverse("account:view-profile")
            )

        user = User.objects.get(username="jdoe")
        self.assertEqual(user.username, "jdoe")
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.userprofile.address.street_1, data["street_1"])
        self.assertEqual(user.userprofile.address.street_2, data["street_2"])
        self.assertEqual(user.userprofile.address.city, data["city"])
        self.assertEqual(user.userprofile.address.zipcode, data["zipcode"])
        self.assertEqual(user.userprofile.address.country, data["country"])


    def test_edit_profile_invalid_attempt(self):
        data = {
            "first_name" : "Johnny",
            "last_name" : "Doe",
            "email" : "fbloggs@test.com",
        }
        response = self.client.post(
            path=reverse("account:edit-profile"),
            data=data,
            follow=True
        )

        self.assertFalse(response.context["form"].is_valid())
        self.assertFormError(
            response,
            "form",
            "email",
             _("This email address is already used by another user. Please try another one.")
            )


    def test_change_password(self):
        data = {
            "old_password" : "jdoe_pwd",
            "new_password1" : "new_jdoe_pwd",
            "new_password2" : "new_jdoe_pwd",
        }
        response = self.client.post(
            path=reverse("account:password-change"),
            data=data,
            follow=True
        )

        self.assertEqual(
            response.redirect_chain[-1][0],
            reverse("account:password-change-done")
            )

        user = User.objects.get(username="jdoe")
        self.assertTrue(user.check_password(data["new_password1"]))


    def test_logout(self):
        response = self.client.get(
            path=reverse("account:logout"),
            follow=True
        )
        self.assertEqual(
            response.redirect_chain[-1][0],
            settings.LOGOUT_REDIRECT_URL
            )
