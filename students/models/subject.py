from django.db import models
from .commonfields import CommonFields
# from .class_studn import ClassName
from django.utils.translation import gettext_lazy as _

class Subjects(CommonFields):

    name = models.CharField(
        _("Name"), max_length=255, null=True
    )
    code = models.CharField(
        _("Code"), max_length=255, null=True
    )
    class_nm = models.ForeignKey(
        'ClassName', on_delete = models.SET_NULL, null=True,
        verbose_name="Class Names", related_name="clss_nme"
    )
    def __str__(self):
        return self.name
