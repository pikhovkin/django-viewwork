from django.conf import settings
from django.core.signals import setting_changed


ADD_USER_MENU = getattr(settings, 'VW_ADD_USER_MENU', True)
ADD_ADMIN_SITE = getattr(settings, 'VW_ADD_ADMIN_SITE', True)
ADD_USER_LOGOUT = getattr(settings, 'VW_ADD_USER_LOGOUT', True)
ADMIN_SITE_URL = getattr(settings, 'VW_ADMIN_SITE_URL', '/admin/')
VW_PREFIX = getattr(settings, 'VW_PREFIX', '')
REMOVE_EMPTY_ITEM = getattr(settings, 'VW_REMOVE_EMPTY_ITEM', True)
USE_APP_NAMESPACE = getattr(settings, 'VW_USE_APP_NAMESPACE', True)


def reload_settings(setting, value, **kwargs):
    if setting == 'VW_REMOVE_EMPTY_ITEM':
        global REMOVE_EMPTY_ITEM
        REMOVE_EMPTY_ITEM = value
    elif setting == 'VW_PREFIX':
        global VW_PREFIX
        VW_PREFIX = value


setting_changed.connect(reload_settings)
