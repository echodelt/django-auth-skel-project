# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'account'

urlpatterns = [

    url(r'^$', views.view_profile, name='home'),

    url(r'^sign-up/$', views.register_minimal, name='register'),
    url(r'^sign-up-confirmation/$', views.register_confirm, name='register-confirm'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^profile/$', views.view_profile, name='view-profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit-profile'),

    url(r'^password-change/$', views.password_change, name='password-change'),
    url(r'^password-change/done/$', views.password_change_done, name='password-change-done'),

    url(r'^password-reset/$', views.password_reset, name='password-reset'),
    url(r'^password-reset/done/$', views.password_reset_done, name='password-reset-done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, name='password-reset-confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password-reset-complete'),

]
