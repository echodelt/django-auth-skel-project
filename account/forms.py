# -*- coding: utf-8 -*-

import logging
LOGGER = logging.getLogger(__name__)

from django import forms

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

import django.contrib.auth.forms as django_auth_forms

from django.core.validators import MinLengthValidator
from django.contrib.auth import password_validation


class NameForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(
        label='First name',
        max_length=100,
        validators=[
            MinLengthValidator(2)
            ],
        required = False
        )

    last_name = forms.CharField(
        label='Last name',
        max_length=100,
        validators=[
            MinLengthValidator(2)
            ],
        required = False
        )


class EmailForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label='Email',
        max_length=100,
        required = True
        )


class AddressForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

    street_1 = forms.CharField(
        label='Street (1)',
        max_length=100,
        required = False
        )

    street_2 = forms.CharField(
        label='Street (2)',
        max_length=100,
        required = False
        )

    city = forms.CharField(
        label='City',
        max_length=100,
        required = False
        )

    zipcode = forms.CharField(
        label='Zip code',
        max_length=100,
        required = False
        )

    country = forms.CharField(
        label='Country',
        max_length=100,
        required = False
        )


class SetPasswordForm(forms.Form):

    custom_set_password_form_err_msgs = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        required = True
        )

    password2 = forms.CharField(
        label='Password (confirm)',
        widget=forms.PasswordInput,
        required = True
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.custom_set_password_form_err_msgs['password_mismatch']
            )
        password_validation.validate_password(password2)
        # used validators defined in settings.AUTH_PASSWORD_VALIDATORS
        return password2


class UserMinimalRegistrationForm(NameForm, EmailForm, SetPasswordForm):

    user_form_err_msgs = {
        'unselectable_username': _("This username already exists. Please try another one."),
        'unselectable_email': _("This email address is already used by another user. Please try another one."),
    }

    def __init__(self, *args, **kwargs):
        super(UserMinimalRegistrationForm, self).__init__(*args, **kwargs)

    username = forms.CharField(
        label='Username',
        max_length=100,
        required = True,
        validators=[
            MinLengthValidator(3)
            ]
        )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.user_form_err_msgs['unselectable_username'])
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(self.user_form_err_msgs['unselectable_email'])
        return email


class UserAccountEditionForm(NameForm, EmailForm, AddressForm):

    user_profile_edit_form_err_msgs = {
        'unselectable_email': _("This email address is already used by another user. Please try another one."),
    }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserAccountEditionForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.user.username
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(self.user_profile_edit_form_err_msgs['unselectable_email'])
        return email


class CustomLoginForm(django_auth_forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)


class CustomPasswordChangeForm(django_auth_forms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_password2'].label = _("New password (confirm)")


class CustomPasswordResetForm(django_auth_forms.PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)


class CustomChangePasswordForm(django_auth_forms.SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
