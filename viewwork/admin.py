from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Menu
from .forms import MenuAdminForm


class ParentListFilter(admin.SimpleListFilter):
    title = _('Parent menu item')
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        return [
            (m.id, m.name)
            for m in Menu.objects.filter(
                view=''
            ).select_related('parent').order_by('name')
        ]

    def queryset(self, request, queryset):
        val = self.value()
        if val:
            return queryset.filter(parent=val)


class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    list_display = ('parent', 'name', 'view', 'sort_order',)
    list_editable = ('sort_order', 'view')
    list_display_links = ('name',)
    list_filter = (ParentListFilter,)
    search_fields = ['name', 'view',]
    ordering = ('parent', 'name', 'sort_order',)


admin.site.register(Menu, MenuAdmin)
