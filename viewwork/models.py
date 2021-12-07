from modeltrans.fields import TranslationField

from django.db import models
from django.utils.translation import gettext_lazy as _


__all__ = (
    'Menu',
)


class Menu(models.Model):
    parent = models.ForeignKey(
        'self', related_name='%(class)s_parent', verbose_name=_('Parent menu item'),
        null=True, blank=True, on_delete=models.PROTECT)
    name = models.CharField(_('Menu item name'), max_length=80)
    view = models.CharField(_('View'), max_length=125, default='', db_index=True)
    sort_order = models.SmallIntegerField(_('Sort order'), default=0)
    hidden = models.BooleanField(_('Hidden item'), default=True, db_index=True)
    enabled = models.BooleanField(_('Enabled item'), default=True, db_index=True)

    i18n = TranslationField(fields=('name',))

    class Meta:
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')
        permissions = [
            ('view_full_access', _('View full access')),
            ('view_read_only', _('View read only')),
        ]

    def __str__(self):
        return self.name_i18n
