from django.conf import settings


ADD_USER_MENU = getattr(settings, 'VW_ADD_USER_MENU', True)
ADD_ADMIN_SITE = getattr(settings, 'VW_ADD_ADMIN_SITE', True)
ADD_USER_LOGOUT = getattr(settings, 'VW_ADD_USER_LOGOUT', True)
ADMIN_SITE_URL = getattr(settings, 'VW_ADMIN_SITE_URL', '/admin/')
VW_PREFIX = getattr(settings, 'VW_PREFIX', '')
REMOVE_EMPTY_ITEM = getattr(settings, 'VW_REMOVE_EMPTY_ITEM', True)
