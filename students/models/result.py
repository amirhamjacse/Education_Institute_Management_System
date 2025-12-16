from django.db import models
from decimal import Decimal as D
from .commonfields import CommonFields
from django.utils.translation import gettext_lazy as _
from .class_studn import ClassName, SectionClas
from .subject import Subjects
from .exam import Exam, ExamYear
# from .students_info import StudentsInfo
class ResultInfo(CommonFields):
    name = models.CharField(
        _("Name"), max_length=255, null=True
    )
    marks = models.DecimalField(
        _("Marks"), decimal_places=2,
        max_digits=12, default=D('0')
    )
    class_name = models.ForeignKey(
        ClassName, on_delete = models.SET_NULL, null=True,
        verbose_name="Class", related_name="classes_name"
    )
    subject = models.ForeignKey(
        Subjects, on_delete = models.SET_NULL, null=True,
        verbose_name="Subject", related_name="subject_name"
    )
    section = models.ForeignKey(
        SectionClas, on_delete = models.SET_NULL, null=True,
        verbose_name="Section", related_name="section_name"
    )
    exam_type = models.ForeignKey(
        Exam, on_delete = models.SET_NULL, null=True,
        verbose_name="Exam Type", related_name="exams"
    )
    exam_year = models.ForeignKey(
        ExamYear, on_delete = models.SET_NULL, null=True,
        verbose_name="Exam Year", related_name="exam_years"
    )
    student = models.ForeignKey(
        'StudentsInfo', on_delete = models.SET_NULL, null=True,
        verbose_name="Students", related_name="stnd"
    )
    
    def __str__(self):
        return f"{self.name} {self.exam_year}"
