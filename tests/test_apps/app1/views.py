from django.http import HttpResponse

from viewwork import BaseViewWork


class Page(BaseViewWork):
    vw_name = 'test_app_vw_page'

    def get(self, request, **kwargs):
        return HttpResponse('Test app1 page')
