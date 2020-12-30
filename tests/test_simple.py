import json

from django.test import TestCase

from viewwork.models import Menu
from viewwork import settings


class TestSimple(TestCase):
    def test_get_empty_menu(self):
        response = self.client.get('/menu/')
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(json.loads(response.content)) == 0)

    def test_get_simple_menu(self):
        Menu.objects.create(name='Test item', view=settings.ADMIN_SITE_URL)

        response = self.client.get('/menu/')
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(json.loads(response.content)) == 1)
