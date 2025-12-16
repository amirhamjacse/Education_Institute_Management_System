from django.db import models
from .commonfields import CommonFields
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .class_studn import ClassName, SectionClas, ClassYear
from students.models.exam import Exam, ExamYear
from students.models.result import ResultInfo
from students.models.subject import Subjects

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
)


RELIGION = (
    ('islam', 'Islam'),
    ('hindu', 'Hindu'),
    ('boudho', 'Boddho'),
    ('christan', 'Christan'),
    ('other', 'Other'),
)

class StudentsInfo(CommonFields):
    name = models.CharField(
        _("Name"), max_length=255, null=True
    )
    unique_roll = models.CharField(
        _('Unique Roll'), max_length=100,
        unique=True, blank=True, null=True
    )
    father_name = models.CharField(
        _("Father's Name"), max_length=255, null=True
    )
    mother_name = models.CharField(
        _("Mother's Name"), max_length=255, null=True
    )
    students_image = models.FileField(
        upload_to='Students_image/%Y/%m/%d/',
        null=True
    )
    date_of_birth = models.DateField(
        _("Date of birth"), null=True
    )
    present_address = models.TextField(
        _("Present Address"), max_length=255, null=True
    )
    permanent_address = models.TextField(
        _("Permanent Address"), max_length=255, null=True
    )
    personal_mobile_number = models.CharField(
        _('Personal Number'), max_length=12, blank=True, null=True,
        validators=[RegexValidator(  # min: 10, max: 12 characters
            r'^[\d]{10,12}$', message='Format (ex: 0173456789)'
        )]
    )
    blood_group = models.CharField(
        _("Blood Group Name"), max_length=10, null=True,
        blank=True
    )
    gurdian_mobile_number = models.CharField(
        _('Gurdian Number'), max_length=12, blank=True, null=True,
        validators=[RegexValidator(  # min: 10, max: 12 characters
            r'^[\d]{10,12}$', message='Format (ex: 0173456789)'
        )]
    )
    admission_date = models.DateField(
        _('Admission Date'), null=True, blank=True
    )
    gender = models.CharField(
        _("Gender"), max_length=12, choices=GENDER,
        default='male'
    )
    relegion = models.CharField(
        _("Relegion"), max_length=12, choices=RELIGION,
        default='islam'
    )
    session = models.CharField(
        _("Session"), max_length=12, blank=True,
        null=True
    )
    class_name =  models.ForeignKey(
        ClassName, on_delete = models.SET_NULL, null=True,
        verbose_name="Class", related_name='class_name'
    )
    section_class =  models.ForeignKey(
        SectionClas, on_delete = models.SET_NULL, null=True,
        verbose_name="Section", related_name='section'
    )
    exam =  models.ForeignKey(
        Exam, on_delete = models.SET_NULL, null=True,
        verbose_name="Exam", related_name="exam"
    )
    # result_info =  models.ForeignKey(
    #     ResultInfo, on_delete = models.SET_NULL, null=True,
    #     verbose_name="Result Info", related_name="resulta_info"
    # )
    subjects =  models.ForeignKey(
        Subjects, on_delete = models.SET_NULL, null=True,
        verbose_name="Result Info", related_name="subjects"
    )


    def __str__(self):
        return self.name
