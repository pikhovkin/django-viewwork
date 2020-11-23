from django.views.generic import View
from django.db.models import F
from django.http import JsonResponse
from django.urls import reverse

from .models import Menu
from .utils import build_nested_tree


__all__ = (
    'MenuView',
    'menu',
)


class MenuView(View):
    http_method_names = ['get']

    def get(self, request):
        menu_items = Menu.objects.all().values(
            'id', 'parent_id', 'name', url=F('view')
        ).order_by('parent_id', 'sort_order', 'name')
        data = []
        for item in menu_items:
            if item['url']:
                item['url'] = reverse(item['url'])
            data.append(item)
        tree = build_nested_tree(data)
        return JsonResponse(tree, safe=False)


menu = MenuView.as_view()
