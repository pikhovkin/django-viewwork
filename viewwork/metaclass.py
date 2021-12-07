import re
import sys

from django.apps import apps
from django.utils.translation import gettext_lazy as _


__all__ = (
    'MetaViewWork',
    'resolver',
)


class MetaViewWork(type):
    @staticmethod
    def _get_class_app(cls):
        app_name = ''
        for module in cls.__module__.split('.'):
            app_name += module
            if f'{app_name}.apps' in sys.modules and apps.is_installed(app_name):
                break
            app_name += '.'
        try:
            return app_name and next(ac for ac in apps.app_configs.values() if ac.name == app_name) or None
        except (StopIteration, IndexError):
            ...
        return None

    def __new__(cls, name, bases, attrs):
        new_cls = super(MetaViewWork, cls).__new__(cls, name, bases, attrs)

        if new_cls.__dict__.get('vw_abstract', False):
            return new_cls

        vw_name = new_cls.__dict__.get('vw_name', getattr(new_cls, 'vw_name', ''))
        vw_verbose_name = getattr(new_cls, 'vw_verbose_name', '')
        cls_name = filter(bool, re.split('(?=[A-Z])', new_cls.__name__))
        if not (vw_name or vw_verbose_name):
            return new_cls
        elif not vw_name:
            vw_name = '_'.join(cls_name).lower()
            new_cls.vw_name = vw_name
        elif not vw_verbose_name:
            new_cls.vw_verbose_name = _(' '.join(cls_name))

        app = cls._get_class_app(new_cls)
        if app:
            vw_prefix = getattr(new_cls, 'vw_prefix', '').strip()
            new_cls.vw[app.label][vw_name] = new_cls
            new_cls.vw[app.label][f'{vw_prefix}{vw_name}'] = new_cls

        return new_cls


def resolver(*classes, **options):
    """Metaclass resolver

    Example:
        SomeClass(resolver(SomeMixin, SomeBaseClass, ..., some_generic_field=..., ...)):
            ...

    :param classes:
    :param options:
    :return: generic metaclass
    """
    is_not_type = lambda cls: cls is not type
    generic_name = lambda gc: '_'.join(c.__name__ for c in gc)
    metaclass = tuple(set(filter(is_not_type, map(type, classes))))
    metaclass = (
        metaclass[0] if len(metaclass) == 1
        else type(generic_name(metaclass), metaclass, options)
    )
    return metaclass(generic_name(classes), classes, options)
