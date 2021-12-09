from operator import attrgetter, itemgetter
import sys

from django import forms
from django.apps import apps
from django.conf import settings
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _, get_language

from modeltrans.utils import build_localized_fieldname
try:
    from easy_select2 import Select2
except (ImportError, ModuleNotFoundError):
    Select2 = forms.Select

from . import BaseViewWork, settings
from .models import Menu


__all__ = (
    'MenuAdminForm',
)


class MenuAdminForm(forms.ModelForm):
    view = forms.ChoiceField(label=_('View'), required=False, widget=Select2())

    def __init__(self, *args, **kwargs):
        super(MenuAdminForm, self).__init__(*args, **kwargs)

        view_choices= []
        vw_prefix = attrgetter('vw_prefix')
        item1 = itemgetter(1)
        for app_label, opts in BaseViewWork.vw.items():
            app = apps.get_app_config(app_label)
            urls = sys.modules[f'{app.module.__name__}.urls']
            namespace = getattr(urls, 'app_name', None) or app.module.__name__
            namespace = f'{namespace}:' if settings.USE_APP_NAMESPACE else ''
            views = filter(lambda v: not vw_prefix(v[1]) or not v[0].startswith(vw_prefix(v[1])), opts.items())
            views = list(map(item1, views))
            options = [(f'{namespace}{v.vw_name}', f'{v.vw_verbose_name}: {v.vw_name}') for v in views]
            options.sort(key=item1)
            view_choices.append((app.verbose_name, options))

        view_choices.sort(key=lambda opt: opt[0])
        view_choices.insert(0, BLANK_CHOICE_DASH[0])

        self.fields['view'].choices = view_choices
        self.fields['parent'].queryset = Menu.objects.filter(view='').order_by('name_i18n')
        self.fields['name_i18n'].required = True

    class Meta:
        model = Menu
        fields = '__all__'
        exclude = ('name',)
        widgets = {
            'parent': Select2()
        }

    @staticmethod
    def _strip(value):
        return (value or '').strip()

    def clean_name_i18n(self):
        return self._strip(self.cleaned_data.get('name_i18n'))

    def clean(self):
        cleaned_data = super().clean()
        for lang in {get_language(), settings.LANGUAGE_CODE}:
            field_name = build_localized_fieldname('name', lang)
            cleaned_data[field_name] = self._strip(cleaned_data.get(field_name)) or cleaned_data.get('name_i18n', '')
        return cleaned_data
