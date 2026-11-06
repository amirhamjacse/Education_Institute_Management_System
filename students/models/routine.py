from django.db import models
from django.utils.translation import gettext_lazy as _
from .commonfields import CommonFields
from .class_studn import ClassName, SectionClas, ClassYear
from .subject import Subjects
from .exam import Exam, ExamYear
from .students_info import StudentsInfo


DAY_CHOICES = [
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]


class TimeSlot(CommonFields):
    """Academic period/time slot model"""
    period_name = models.CharField(_('Period Name'), max_length=50)  # e.g., 1st Period
    start_time = models.TimeField(_('Start Time'))
    end_time = models.TimeField(_('End Time'))
    is_break = models.BooleanField(_('Is Break/Tiffin'), default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        start = self.start_time.strftime('%I:%M %p') if self.start_time else ''
        end = self.end_time.strftime('%I:%M %p') if self.end_time else ''
        return f"{self.period_name} ({start} - {end})"


class TeacherAssignment(CommonFields):
    """Maps teachers to their designated class, section, and subject"""
    teacher = models.ForeignKey(
        'institute_dashaboard.Teachers_Information',
        on_delete=models.CASCADE,
        related_name='assigned_classes'
    )
    class_name = models.ForeignKey(
        ClassName,
        on_delete=models.CASCADE,
        related_name='teacher_assignments'
    )
    section = models.ForeignKey(
        SectionClas,
        on_delete=models.CASCADE,
        related_name='teacher_assignments'
    )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='teacher_assignments'
    )
    academic_year = models.ForeignKey(
        ClassYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('teacher', 'class_name', 'section', 'subject')

    def __str__(self):
        return f"{self.teacher.teachers_name} - {self.class_name.name} ({self.section.name}) [{self.subject.name}]"


class ClassRoutine(CommonFields):
    """Visual weekly timetable schedule per class and section"""
    class_name = models.ForeignKey(
        ClassName,
        on_delete=models.CASCADE,
        related_name='routines'
    )
    section = models.ForeignKey(
        SectionClas,
        on_delete=models.CASCADE,
        related_name='routines'
    )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        related_name='routines'
    )
    teacher = models.ForeignKey(
        'institute_dashaboard.Teachers_Information',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='routines'
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='routines'
    )
    day_of_week = models.CharField(_('Day of Week'), max_length=20, choices=DAY_CHOICES)
    room_number = models.CharField(_('Room Number'), max_length=50, default='Room 101')

    class Meta:
        ordering = ['day_of_week', 'time_slot__start_time']
        unique_together = ('class_name', 'section', 'time_slot', 'day_of_week')

    def __str__(self):
        return f"{self.class_name.name}-{self.section.name} | {self.day_of_week} | {self.time_slot.period_name} | {self.subject.name}"


class ExamAdmitCard(CommonFields):
    """Exam admit card with room and seat allocation"""
    student = models.ForeignKey(
        StudentsInfo,
        on_delete=models.CASCADE,
        related_name='admit_cards'
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='admit_cards'
    )
    exam_year = models.ForeignKey(
        ExamYear,
        on_delete=models.CASCADE,
        related_name='admit_cards'
    )
    roll_number = models.CharField(_('Exam Roll Number'), max_length=50)
    room_number = models.CharField(_('Room Number'), max_length=50, blank=True, default='')
    seat_bench = models.CharField(_('Bench / Seat Number'), max_length=50, blank=True, default='')
    instructions = models.TextField(
        _('Instructions'),
        blank=True,
        default='1. Bring this admit card to the examination hall.\n2. Arrive at least 15 minutes before exam starts.\n3. Mobile phones and unauthorized materials are strictly prohibited.'
    )
    is_approved = models.BooleanField(_('Is Approved'), default=True)

    class Meta:
        unique_together = ('student', 'exam', 'exam_year')

    def __str__(self):
        return f"Admit Card: {self.student.name} (Roll: {self.roll_number}) - {self.exam.name}"
