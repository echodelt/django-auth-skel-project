# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User

FIXTURES = ["test_data"]

class BaseTest(TestCase):
    fixtures = FIXTURES

    def setUp(self):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
        # from :
        # http://stackoverflow.com/questions/8017204/users-in-initial-data-fixture
