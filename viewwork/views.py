from django.views.generic import View
from django.http import JsonResponse
from django.urls import reverse, NoReverseMatch

from .models import Menu
from .utils import build_nested_tree


__all__ = (
    'MenuView',
    'menu',
)


class MenuView(View):
    http_method_names = ['get']

    def get_queryset(self):
        return Menu.objects.all().values(
            'id', 'parent_id', 'name', 'view'
        ).order_by('parent_id', 'sort_order', 'name')

    def get(self, request, *args, **kwargs):
        menu_items = self.get_queryset()
        data = []
        for item in menu_items:
            if item['view']:
                try:
                    item['url'] = reverse(item['view'])
                except NoReverseMatch:
                    continue
            data.append(item)
        tree = build_nested_tree(data)
        return JsonResponse(tree, safe=False)


menu = MenuView.as_view()
