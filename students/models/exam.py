from django.db import models
from .commonfields import CommonFields
from django.utils.translation import gettext_lazy as _

class Exam(CommonFields):
    name = models.CharField(
        _("Name"), max_length=255, null=True
    )
    exam_yea = models.ForeignKey(
        'ExamYear', on_delete = models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name

class ExamYear(CommonFields):
    exam_year = models.CharField(
        _("Exam Year"), max_length=15, null=True
    )
    date = models.DateField(
        _("Date of Exam"), null=True
    )
    
    def __str__(self):
        return self.exam_year