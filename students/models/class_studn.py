from django.db import models
from .commonfields import CommonFields
from django.utils.translation import gettext_lazy as _
from .subject import Subjects


class ClassName(CommonFields):
    name = models.CharField(
        _("Name"), max_length=255, null=True
    )
    code = models.CharField(
        _("Code"), max_length=255, null=True
    )
    class_nm = models.ForeignKey(
        'ClassYear', on_delete = models.SET_NULL, null=True,
        verbose_name="Class Year", related_name="cls_yr"
    )


    def __str__(self):
        return self.name


class ClassYear(CommonFields):
    class_year = models.CharField(
        _("Class Year"), max_length=15, null=True
    )
    # date = models.DateField(
    #     _("Date of Exam"), null=True
    # )
    def __str__(self):
        return self.class_year

class SectionClas(CommonFields):
    class_nm = models.ForeignKey(
        ClassName, on_delete = models.SET_NULL, null=True,
        verbose_name="Class Name", related_name="cls_nm"
    )
    name = models.CharField(
        _("Name"), max_length=255, null=True
    )
    code = models.CharField(
        _("Code"), max_length=255, null=True
    )
    def __str__(self):
        return self.name


class Session(CommonFields):
    name = models.CharField(
        _("Name"), max_length=255, null=True
    )

    def __str__(self):
        return self.name

