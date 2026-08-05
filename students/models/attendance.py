from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from .commonfields import CommonFields
from .students_info import StudentsInfo
from .class_studn import ClassName, SectionClas

STATUS_CHOICES = (
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('leave', 'Leave'),
)


class Attendance(CommonFields):
    student = models.ForeignKey(
        StudentsInfo, on_delete=models.CASCADE,
        verbose_name="Student", related_name="attendances"
    )
    class_name = models.ForeignKey(
        ClassName, on_delete=models.SET_NULL, null=True,
        verbose_name="Class", related_name="attendance_records"
    )
    section = models.ForeignKey(
        SectionClas, on_delete=models.SET_NULL, null=True,
        verbose_name="Section", related_name="attendance_records"
    )
    date = models.DateField(_("Date"))
    status = models.CharField(
        _("Status"), max_length=10, choices=STATUS_CHOICES,
        default='present'
    )
    remarks = models.CharField(
        _("Remarks"), max_length=255, blank=True, null=True
    )
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="Marked By",
        related_name="attendance_marked"
    )

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"
