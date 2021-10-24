from django.contrib import admin
from django.utils.translation import gettext_lazy as _, get_language

from modeltrans.utils import build_localized_fieldname
try:
    from guardian.admin import GuardedModelAdmin as ModelAdmin
except (ImportError, ModuleNotFoundError):
    ModelAdmin = admin.ModelAdmin

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
            ).select_related('parent').order_by('name_i18n')
        ]

    def queryset(self, request, queryset):
        val = self.value()
        if val:
            return queryset.filter(parent=val)


class MenuAdmin(ModelAdmin):
    form = MenuAdminForm
    list_display = ('parent', 'name_i18n', 'view', 'sort_order',)
    list_editable = ('sort_order',)
    list_display_links = ('name_i18n',)
    list_filter = (ParentListFilter,)
    search_fields = ('name_i18n', 'view',)
    ordering = ('parent', 'name_i18n', 'sort_order',)
    exclude = ('name',)

    def get_exclude(self, request, obj=None):
        excludes = set(super().get_exclude(request) or [])
        excludes.add(build_localized_fieldname('name', get_language()))
        return list(excludes)


admin.site.register(Menu, MenuAdmin)
