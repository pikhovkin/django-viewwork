import json

from django.conf import settings as dj_settings
from django.test import TestCase, override_settings
from django.urls import reverse, exceptions

from viewwork.models import Menu
from viewwork import settings

from . import menu_id_list


class TestSimple(TestCase):
    def test_get_empty_menu(self):
        response = self.client.get('/menu/')
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(json.loads(response.content)) == 0)

    def test_get_simple_menu(self):
        Menu.objects.create(name='Test item', view=settings.ADMIN_SITE_URL, hidden=False)

        response = self.client.get('/menu/')
        self.assertContains(response, 'Test item')
        self.assertTrue(len(json.loads(response.content)) == 1)

    def test_hidden_menu_item(self):
        Menu.objects.create(name='Test item', view=settings.ADMIN_SITE_URL, hidden=True)

        response = self.client.get('/menu/')
        self.assertContains(response, '[]')
        self.assertTrue(len(json.loads(response.content)) == 0)

    def test_disabled_menu_item(self):
        Menu.objects.create(name='Test item', view=settings.ADMIN_SITE_URL, hidden=False, enabled=False)

        response = self.client.get('/menu/')
        self.assertContains(response, '[]')
        self.assertTrue(len(json.loads(response.content)) == 0)

    @override_settings(
        VW_REMOVE_EMPTY_ITEM=True,
    )
    def test_nested_tree(self):
        p1 = Menu.objects.create(name='Section1', hidden=False)
        p2 = Menu.objects.create(name='Section2', parent=p1, hidden=False)
        p3 = Menu.objects.create(name='Section3', parent=p2, hidden=False)
        p4 = Menu.objects.create(name='Section3', hidden=False)
        item1 = Menu.objects.create(name='Test admin site', view=settings.ADMIN_SITE_URL, parent=p4, hidden=False)
        item2 = Menu.objects.create(name='Test app page', view='test_app_page', hidden=False)

        response = self.client.get('/menu/')
        ids = menu_id_list(json.loads(response.content))
        self.assertTrue(p1.pk not in ids)
        self.assertTrue(p2.pk not in ids)
        self.assertTrue(p3.pk not in ids)
        self.assertTrue(p4.pk in ids)
        self.assertTrue(item1.pk in ids)
        self.assertTrue(item2.pk in ids)

    @override_settings(
        VW_REMOVE_EMPTY_ITEM=True,
    )
    def test_deep_nested_tree(self):
        p1 = Menu.objects.create(name='Section1', hidden=False)
        p2 = Menu.objects.create(name='Section2', parent=p1, hidden=False)
        p3 = Menu.objects.create(name='Section3', parent=p2, hidden=False)
        p4 = Menu.objects.create(name='Section4', parent=p3, hidden=False)
        item1 = Menu.objects.create(name='Test admin site', view=settings.ADMIN_SITE_URL, parent=p4, hidden=False)
        item2 = Menu.objects.create(name='Test app page', view='test_app_page', hidden=False)

        response = self.client.get('/menu/')
        ids = menu_id_list(json.loads(response.content))
        self.assertTrue(p1.pk in ids)
        self.assertTrue(p2.pk in ids)
        self.assertTrue(p3.pk in ids)
        self.assertTrue(p4.pk in ids)
        self.assertTrue(item1.pk in ids)
        self.assertTrue(item2.pk in ids)

    @override_settings(
        VW_REMOVE_EMPTY_ITEM=False,
    )
    def test_nested_empty_tree(self):
        p1 = Menu.objects.create(name='Section1', hidden=False)
        p2 = Menu.objects.create(name='Section2', parent=p1, hidden=False)
        p3 = Menu.objects.create(name='Section3', parent=p2, hidden=False)
        p4 = Menu.objects.create(name='Section4', parent=p3, hidden=False)
        item1 = Menu.objects.create(name='Test admin site', view=settings.ADMIN_SITE_URL, hidden=False)
        item2 = Menu.objects.create(name='Test app page', view='test_app_page', hidden=False)

        response = self.client.get('/menu/')
        ids = menu_id_list(json.loads(response.content))
        self.assertTrue(p1.pk in ids)
        self.assertTrue(p2.pk in ids)
        self.assertTrue(p3.pk in ids)
        self.assertTrue(p4.pk in ids)
        self.assertTrue(item1.pk in ids)
        self.assertTrue(item2.pk in ids)

    @override_settings(
        MIDDLEWARE=dj_settings.MIDDLEWARE + ['django.middleware.locale.LocaleMiddleware'],
        USE_I18N=True,
        LANGUAGE_CODE='en',
        LANGUAGES=(('en', 'English'), ('es', 'Español')),
    )
    def test_i18n_menu(self):
        p1 = Menu.objects.create(name='Section1', name_es='Sección1', hidden=False)
        p2 = Menu.objects.create(name='Section2', name_es='Sección2', parent=p1, hidden=False)
        Menu.objects.create(name='Test page', name_es='Página de prueba', view='test_app_page', parent=p2, hidden=False)

        response = self.client.get('/menu/')
        self.assertContains(response, 'Section1')
        self.assertContains(response, 'Section2')
        self.assertContains(response, 'Test page')

        self.client.post('/i18n/setlang/', {'language': 'es'})
        response = self.client.get('/menu/')
        self.assertContains(response, 'Secci\\u00f3n1')
        self.assertContains(response, 'Secci\\u00f3n2')
        self.assertContains(response, 'P\\u00e1gina de prueba')

        self.client.post('/i18n/setlang/', {'language': 'ru'})
        response = self.client.get('/menu/')
        self.assertContains(response, 'Section1')
        self.assertContains(response, 'Section2')
        self.assertContains(response, 'Test page')

    def test_url_pages_with_prefix(self):
        item1 = Menu.objects.create(name='Test app page', view='tests.testapp:test_app_vw_page', hidden=False)
        item2 = Menu.objects.create(name='Test app1 page', view='viewwork_tests_test_apps_app1:test_app_vw_page', hidden=False)
        item3 = Menu.objects.create(name='Test app2 page', view='tests.test_apps.app2:test_app_vw_page', hidden=False)

        response = self.client.get('/menu/')
        menu = {item['id']: item['_url'] for item in json.loads(response.content)}
        self.assertTrue(menu[item1.id] == f'/app/{settings.VW_PREFIX}test_app_vw_page/')
        self.assertTrue(menu[item2.id] == f'/app1/{settings.VW_PREFIX}test_app_vw_page/')
        self.assertTrue(menu[item3.id] == f'/app2/{settings.VW_PREFIX}test_app_vw_page/')


class TestAppView(TestCase):
    def test_func_page(self):
        response = self.client.get('/app/page/')
        self.assertContains(response, 'Test page')

    def test_cbv_page(self):
        response = self.client.get('/app/test_app_vw_page/')
        self.assertContains(response, 'Test app page')

        response = self.client.get(reverse('tests.testapp:test_app_vw_page'))
        self.assertContains(response, 'Test app page')


class TestAppsView(TestCase):
    def test_app1_page(self):
        response = self.client.get('/app1/test_app_vw_page/')
        self.assertContains(response, 'Test app1 page')

        response = self.client.get(reverse('viewwork_tests_test_apps_app1:test_app_vw_page'))
        self.assertContains(response, 'Test app1 page')

        with self.assertRaises(exceptions.NoReverseMatch):
            reverse('test_app_vw_page')
        with self.assertRaises(exceptions.NoReverseMatch):
            reverse('tests.test_apps.app1:test_app_vw_page')

    def test_app2_page(self):
        response = self.client.get('/app2/test_app_vw_page/')
        self.assertContains(response, 'Test app2 page')

        response = self.client.get(reverse('tests.test_apps.app2:test_app_vw_page'))
        self.assertContains(response, 'Test app2 page')

        response = self.client.get(reverse('tests.test_apps.app2:test_app_vw_page'))
        self.assertContains(response, 'Test app2 page')
