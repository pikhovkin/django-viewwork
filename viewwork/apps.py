from pathlib import Path
from importlib import import_module
import pkgutil

from django.apps import AppConfig, apps
from django.utils.translation import gettext_lazy as _
from django.urls import path

from . import BaseViewWork


__all__ = (
    'ViewWorkConfig',
)


class ViewWorkConfig(AppConfig):
    name: str = 'viewwork'
    verbose_name: str = _('ViewWork')

    def collect_urls(self, app: AppConfig):
        urlpatterns = [
            path(f'{name}/', view_class.as_view(), name=name)
            for name, view_class in BaseViewWork.vw['all_views'].items()
        ]
        urls = import_module(f'{app.module.__name__}.urls')
        urls.urlpatterns += urlpatterns

    def collect_views(self, app: AppConfig):
        app_name = app.module.__name__
        import_module(f'{app_name}.views')
        for entry in pkgutil.walk_packages([Path(app.path) / 'views'], f'{app_name}.views.'):
            import_module(entry.name)

    def ready(self):
        for app in apps.get_app_configs():
            if getattr(app, 'vw_collect', False):
                self.collect_views(app)
                self.collect_urls(app)
