from django.views.generic import View
from django.http import JsonResponse
from django.urls import reverse, resolve, NoReverseMatch, Resolver404
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.db.models import Q

try:
    from guardian.shortcuts import get_objects_for_user
except (ImportError, ModuleNotFoundError):
    get_objects_for_user = None

from .models import Menu
from .utils import build_nested_tree
from . import settings


__all__ = (
    'MenuView',
    'menu',
)


User = get_user_model()


class MenuView(View):
    http_method_names = ['get']

    def get_queryset(self):
        if not get_objects_for_user or self.request.user.is_superuser:
            menu = Menu.objects.all()
        else:
            menu_items = get_objects_for_user(
                self.request.user, 'viewwork.view_menu'
            ).values_list('pk', flat=True)
            menu = Menu.objects.filter(Q(pk__in=menu_items) | Q(view=''))
        return menu.values(
            'id', 'parent_id', 'name', 'view'
        ).order_by('parent_id', 'sort_order', 'name')

    def patch_tree(self, tree):
        if settings.ADD_USER_MENU and self.request.user.is_authenticated:
            tree.append({
                'id': '-2',
                'parent_id': None,
                'name': getattr(self.request.user, User.USERNAME_FIELD),
                'url': '',
                'items': [
                    {'id': '-3', 'parent_id': '-2', 'name': _('Admin site'), 'url': settings.ADMIN_SITE_URL},
                    {'id': '-4', 'parent_id': '-2', 'name': _('Logout'), 'url': reverse('vw_logout'), 'target': '_self'},
                ],
            })
        return tree

    def get(self, request, *args, **kwargs):
        menu_items = self.get_queryset()
        data = []
        for item in menu_items:
            if item['view']:
                try:
                    item['url'] = reverse(item['view'])
                except NoReverseMatch:
                    try:
                        resolve(item['view'])
                        item['url'] = item['view']
                    except Resolver404:
                        continue
            data.append(item)
        tree = build_nested_tree(data)
        tree = self.patch_tree(tree)
        return JsonResponse(tree, safe=False)


menu = MenuView.as_view()
