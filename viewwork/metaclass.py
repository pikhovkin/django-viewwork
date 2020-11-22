import re

from django.utils.translation import gettext_lazy as _


__all__ = (
    'MetaViewWork',
    'resolver',
)


class MetaViewWork(type):
    def __new__(cls, name, bases, attrs):
        new_cls = super(MetaViewWork, cls).__new__(cls, name, bases, attrs)

        if new_cls.__dict__.get('vw_abstract', False):
            return new_cls

        cls_name = filter(bool, re.split('(?=[A-Z])', new_cls.__name__))

        vw_name = new_cls.__dict__.get('vw_name', getattr(new_cls, 'vw_name', ''))
        vw_verbose_name = getattr(new_cls, 'vw_verbose_name', '')
        dash_prefix = getattr(new_cls, 'vw_prefix', '').strip()

        if not (vw_name or vw_verbose_name):
            return new_cls
        elif not vw_name:
            vw_name = '_'.join(cls_name).lower()
            new_cls.vw_name = vw_name
        elif not vw_verbose_name:
            new_cls.vw_verbose_name = _(' '.join(cls_name))

        new_cls.vw['all_views'][vw_name] = new_cls
        new_cls.vw['all_views'][f'{dash_prefix}{vw_name}'] = new_cls

        return new_cls


def resolver(*classes, **options):
    """Metaclass resolver

    Example:
        SomeClass(resolver(SomeMixin, BaseClass, ..., vw_abstract=True, ...)):
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
