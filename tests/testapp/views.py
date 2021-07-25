from django.http import HttpResponse


def page(request, *args, **kwags):
    return HttpResponse('Test page')
