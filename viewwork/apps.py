from importlib import import_module
from pathlib import Path
import pkgutil

from django.apps import AppConfig, apps
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from . import BaseViewWork, settings


__all__ = (
    'ViewWorkConfig',
)


class ViewWorkConfig(AppConfig):
    name: str = 'viewwork'
    verbose_name: str = _('ViewWork')

    def collect_views(self, app: AppConfig):
        app_name = app.module.__name__
        import_module(f'{app_name}.views')
        for entry in pkgutil.walk_packages([str(Path(app.path) / 'views')], f'{app_name}.views.'):
            import_module(entry.name)

    def collect_urls(self, app: AppConfig):
        urls = import_module(f'{app.module.__name__}.urls')
        app_urls_namespace = getattr(urls, 'app_name', None)
        urlpatterns = [
            path(f'{name}/', view_class.as_view(), name=name)
            for name, view_class in BaseViewWork.vw[app.label].items()
        ]
        if app_urls_namespace or not settings.USE_APP_NAMESPACE:
            urls.urlpatterns += urlpatterns
        else:
            urls.urlpatterns += [path('', include((urlpatterns, app.module.__name__)))]

    def ready(self):
        for app in apps.get_app_configs():
            if not getattr(app, 'vw_collect', False):
                continue

            self.collect_views(app)
            self.collect_urls(app)
