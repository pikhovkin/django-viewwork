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
    view = models.CharField(_('View'), max_length=80, default='')
    sort_order = models.SmallIntegerField(_('Sort order'), default=0)

    class Meta:
        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')

    def __str__(self):
        return self.name
