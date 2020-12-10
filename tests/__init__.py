from django.test import TestCase


class SimpleTest(TestCase):
    def test_get_empty_menu(self):
        response = self.client.get('/menu/')
        self.assertTrue(response.status_code == 200)
