# -*- coding: utf-8 -*-

import logging
LOGGER = logging.getLogger(__name__)

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import views as django_auth_views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction

from . import forms as account_forms
from .models import UserProfile, Address


@transaction.atomic
def get_or_create_profile(user):
    # creates user profile and address for users registered
    # via the regular admin interface
    # (not via the account:login view)
    try:
        userprofile = user.userprofile
    except UserProfile.DoesNotExist:
        userprofile = UserProfile(user=user)
        userprofile.save()
    try:
        address = userprofile.address
    except Address.DoesNotExist:
        address = Address()
        address.userprofile = userprofile
        address.save()
    return userprofile


@csrf_protect
@transaction.atomic
def register_minimal(request):
    if request.method == 'POST':
        form = account_forms.UserMinimalRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=form.cleaned_data['password2'],
                    email=form.cleaned_data['email']
                    )

                userprofile = UserProfile(user=user)
                userprofile.save()

                address = Address(userprofile=userprofile)
                address.save()

                return HttpResponseRedirect(reverse('account:register-confirm'))

            except Exception as e:
                LOGGER.exception(
                    "An exception has occurred while registering a new user : %s : %s" % \
                    (type(e), e)
                    )
                raise

    else:
        form = account_forms.UserMinimalRegistrationForm()

    context = {}
    context["page_title"] = _("Register")
    context["form"] = form

    return render(request, 'account/register-minimal.html', context)


def register_confirm(request):
    context = {}
    context["page_title"] = _("Sign up confirmation")

    return render(request, 'account/register-confirm.html', context)


@csrf_protect
def login(request):
    context = {}
    context["page_title"] = _("Login")

    return django_auth_views.login(
        request,
        template_name='account/login.html',
        extra_context=context,
        authentication_form=account_forms.CustomLoginForm,
        redirect_authenticated_user=True,
        )


def logout(request):
    return django_auth_views.logout(
        request
        )


@login_required
def view_profile(request):
    try:
        user = request.user
        userprofile = get_or_create_profile(user)

    except Exception as e:
        LOGGER.exception(
            "An exception occurred while rendering a user's profile : %s : %s" % \
            (type(e), e)
            )
        raise

    context = {}
    context["page_title"] = _("profile")
    context["user"] = user

    return render(request, 'account/view-profile.html', context)


@login_required
@csrf_protect
@transaction.atomic
def edit_profile(request):
    user = request.user
    userprofile = get_or_create_profile(user)
    if request.method == 'POST':
        form = account_forms.UserAccountEditionForm(user, request.POST)
        if form.is_valid():
            try:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                address = user.userprofile.address
                address.street_1 = form.cleaned_data['street_1']
                address.street_2 = form.cleaned_data['street_2']
                address.city = form.cleaned_data['city']
                address.zipcode = form.cleaned_data['zipcode']
                address.country = form.cleaned_data['country']
                address.save()
                return HttpResponseRedirect(reverse('account:view-profile'))
            except Exception as e:
                LOGGER.exception(
                    "An exception has occurred while updating a user's profile : %s : %s" % \
                    (type(e), e)
                    )
                raise
    else:
        address = user.userprofile.address
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'street_1': address.street_1,
            'street_2': address.street_2,
            'city': address.city,
            'zipcode': address.zipcode,
            'country': address.country,
        }
        form = account_forms.UserAccountEditionForm(
            user,
            initial = initial
            )

    context = {}
    context["page_title"] = _("Edit profile")
    context["form"] = form

    return render(request, 'account/edit-profile.html', context)


@login_required
@csrf_protect
def password_change(request):
    context = {}
    context["page_title"] = _("Password change")

    return django_auth_views.password_change(
        request,
        template_name='account/password-change.html',
        extra_context=context,
        password_change_form=account_forms.CustomPasswordChangeForm,
        post_change_redirect=reverse('account:password-change-done')
        )


@login_required
def password_change_done(request):
    context = {}
    context["page_title"] = _("Password change done")

    return render(request, 'account/password-change-done.html', context)


@csrf_protect
def password_reset(request):
    context = {}
    context["page_title"] = _("Password reset")

    return django_auth_views.password_reset(
        request,
        template_name='account/password-reset.html',
        extra_context=context,
        password_reset_form=account_forms.CustomPasswordResetForm,
        subject_template_name='account/email/password_reset_subject.txt',
        email_template_name='account/email/password-reset-email.html',
        post_reset_redirect=reverse('account:password-reset-done')
        )


def password_reset_done(request):
    context = {}
    context["page_title"] = _("Password reset done")

    return render(request, 'account/password-reset-done.html', context)


@csrf_protect
def password_reset_confirm(request, uidb64, token):
    context = {}
    context["page_title"] = _("Password reset confirm")

    return django_auth_views.password_reset_confirm(
        request,
        uidb64=uidb64,
        token=token,
        template_name='account/password-reset-confirm.html',
        extra_context=context,
        set_password_form=account_forms.CustomChangePasswordForm,
        post_reset_redirect=reverse('account:password-reset-complete')
        )


def password_reset_complete(request):
    context = {}
    context["page_title"] = _("Password reset complete")

    return render(request, 'account/password-reset-complete.html', context)
