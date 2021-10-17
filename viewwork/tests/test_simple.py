import json

from django.test import TestCase

from viewwork.models import Menu
from viewwork import settings

from . import menu_id_list


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

    def test_nested_tree(self):
        setattr(settings, 'REMOVE_EMPTY_ITEM', True)
        p1 = Menu.objects.create(name='Section1')
        p2 = Menu.objects.create(name='Section2', parent=p1)
        p3 = Menu.objects.create(name='Section3', parent=p2)
        p4 = Menu.objects.create(name='Section3')
        item1 = Menu.objects.create(name='Test admin site', view=settings.ADMIN_SITE_URL, parent=p4)
        item2 = Menu.objects.create(name='Test app page', view='test_app_page')

        response = self.client.get('/menu/')
        ids = menu_id_list(json.loads(response.content))
        self.assertTrue(p1.pk not in ids)
        self.assertTrue(p2.pk not in ids)
        self.assertTrue(p3.pk not in ids)
        self.assertTrue(p4.pk in ids)
        self.assertTrue(item1.pk in ids)
        self.assertTrue(item2.pk in ids)

    def test_deep_nested_tree(self):
        setattr(settings, 'REMOVE_EMPTY_ITEM', True)
        p1 = Menu.objects.create(name='Section1')
        p2 = Menu.objects.create(name='Section2', parent=p1)
        p3 = Menu.objects.create(name='Section3', parent=p2)
        p4 = Menu.objects.create(name='Section4', parent=p3)
        item1 = Menu.objects.create(name='Test admin site', view=settings.ADMIN_SITE_URL, parent=p4)
        item2 = Menu.objects.create(name='Test app page', view='test_app_page')

        response = self.client.get('/menu/')
        ids = menu_id_list(json.loads(response.content))
        self.assertTrue(p1.pk in ids)
        self.assertTrue(p2.pk in ids)
        self.assertTrue(p3.pk in ids)
        self.assertTrue(p4.pk in ids)
        self.assertTrue(item1.pk in ids)
        self.assertTrue(item2.pk in ids)

    def test_nested_empty_tree(self):
        setattr(settings, 'REMOVE_EMPTY_ITEM', False)
        p1 = Menu.objects.create(name='Section1')
        p2 = Menu.objects.create(name='Section2', parent=p1)
        p3 = Menu.objects.create(name='Section3', parent=p2)
        p4 = Menu.objects.create(name='Section4', parent=p3)
        item1 = Menu.objects.create(name='Test admin site', view=settings.ADMIN_SITE_URL)
        item2 = Menu.objects.create(name='Test app page', view='test_app_page')

        response = self.client.get('/menu/')
        ids = menu_id_list(json.loads(response.content))
        self.assertTrue(p1.pk in ids)
        self.assertTrue(p2.pk in ids)
        self.assertTrue(p3.pk in ids)
        self.assertTrue(p4.pk in ids)
        self.assertTrue(item1.pk in ids)
        self.assertTrue(item2.pk in ids)


class TestAppView(TestCase):
    def test_func_page(self):
        response = self.client.get('/app/page/')
        self.assertContains(response, 'Test page')

    def test_cbv_page(self):
        response = self.client.get('/app/test_app_vw_page/')
        self.assertContains(response, 'Test app page')


class TestAppsView(TestCase):
    def test_app1_page(self):
        response = self.client.get('/app1/test_app1_vw_page/')
        self.assertContains(response, 'Test app1 page')

    def test_app2_page(self):
        response = self.client.get('/app2/test_app2_vw_page/')
        self.assertContains(response, 'Test app2 page')
