import sys

from django.apps import apps
from django.core.management import BaseCommand

from viewwork import BaseViewWork
from viewwork.models import Menu


class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument('action', action='store', type=str, choices=['add', 'delete'])

    def add(self):
        for app_label, values in BaseViewWork.vw.items():
            app = apps.get_app_config(app_label)
            urls = sys.modules[f'{app.module.__name__}.urls']
            namespace = getattr(urls, 'app_name', None) or app.module.__name__
            for item in Menu.objects.filter(view__in=values.keys()):
                item.view = f'{namespace}:{item.view}'
                item.save(update_fields=('view',))

    def delete(self):
        for item in Menu.objects.filter(view__icontains=':'):
            item.view = item.view.split(':')[1]
            item.save(update_fields=('view',))

    def handle(self, *args, **options):
        if options['action'] == 'add':
            self.add()
        elif options['action'] == 'delete':
            self.delete()
