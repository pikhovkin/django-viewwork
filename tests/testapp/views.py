from django.http import HttpResponse

from viewwork import BaseViewWork


def page(request, *args, **kwags):
    return HttpResponse('Test page')


class Page(BaseViewWork):
    vw_name = 'test_app_vw_page'

    def get(self, request, **kwargs):
        return HttpResponse('Test app page')
