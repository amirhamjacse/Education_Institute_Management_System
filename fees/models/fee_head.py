from django.db import models
from django.utils.translation import gettext_lazy as _

from students.models.commonfields import CommonFields


class FeeHead(CommonFields):
    name = models.CharField(_("Name"), max_length=100)
    code = models.CharField(_("Code"), max_length=20, unique=True)
    description = models.CharField(
        _("Description"), max_length=255, blank=True, null=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
