from django.conf import settings


ADD_USER_MENU = getattr(settings, 'VW_ADD_USER_MENU', True)
ADMIN_SITE_URL = getattr(settings, 'VW_ADMIN_SITE_URL', '/admin/')
