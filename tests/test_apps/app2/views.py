from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from viewwork import BaseViewWork


class Page(BaseViewWork):
    vw_name = 'test_app_vw_page'
    vw_verbose_name = _('App2 page')

    def get(self, request, **kwargs):
        return HttpResponse('Test app2 page')
