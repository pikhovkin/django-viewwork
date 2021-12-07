from django.apps import AppConfig


class TestApp2Config(AppConfig):
    name = 'tests.test_apps.app2'
    label = 'app2'
    verbose_name = 'App2 config'
    vw_collect = True
