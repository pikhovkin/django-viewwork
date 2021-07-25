from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'permissions': [('view_full_access', 'View full access'), ('view_read_only', 'View read only')], 'verbose_name': 'Menu item', 'verbose_name_plural': 'Menu items'},
        ),
    ]
