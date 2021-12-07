import sys

from django.apps import apps as real_apps
from django.db import migrations, models

from viewwork import BaseViewWork


def fix_view_name(apps, schema_editor):
    Menu = apps.get_model('viewwork', 'Menu')

    for app_label, values in BaseViewWork.vw.items():
        app = real_apps.get_app_config(app_label)
        urls = sys.modules[f'{app.module.__name__}.urls']
        namespace = getattr(urls, 'app_name', None) or app.module.__name__
        for item in Menu.objects.filter(view__in=values.keys()):
            item.view = f'{namespace}:{item.view}'
            item.save(update_fields=('view',))


def remove_app_label(apps, schema_editor):
    Menu = apps.get_model('viewwork', 'Menu')

    for item in Menu.objects.filter(view__icontains=':'):
        item.view = item.view.split(':')[1]
        item.save(update_fields=('view',))


class Migration(migrations.Migration):
    dependencies = [
        ('viewwork', '0004_enabled_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='view',
            field=models.CharField(db_index=True, default='', max_length=125, verbose_name='View'),
        ),

        migrations.RunPython(fix_view_name, reverse_code=remove_app_label),
    ]
