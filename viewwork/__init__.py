from collections import defaultdict

from django.views.generic import TemplateView

from .metaclass import resolver as metaclass_resolver, MetaViewWork


__all__ = (
    '__version__',
    'default_app_config',
    'BaseViewWork',
)
__version__ = '0.1.0'


default_app_config = 'viewwork.apps.ViewWorkConfig'


class BaseViewWork(TemplateView, metaclass=MetaViewWork):
    vw = defaultdict(dict)
    vw_abstract = True
