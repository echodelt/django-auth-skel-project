# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse

class ViewTest(TestCase):

    def test_get_homepage(self):
        response = self.client.get(
            path=reverse("homepage"),
            follow=False
        )

        self.assertEqual(response.status_code, 200)
