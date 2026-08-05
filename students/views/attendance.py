import datetime

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from students.forms.attendance import AttendanceQueryForm
from students.models.attendance import Attendance, STATUS_CHOICES
from students.models.class_studn import ClassName, SectionClas
from students.models.students_info import StudentsInfo


class AttendanceQueryView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'attendance/query_for_attendance.html'
    permission_required = 'students.add_attendance'
    form_class = AttendanceQueryForm

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cls = form.cleaned_data['class_name']
            section = form.cleaned_data['section']
            att_date = form.cleaned_data['date']
            return redirect(
                'students:attendance_mark',
                clas_nm=cls.id, clas_sec=section.id,
                att_date=att_date.isoformat()
            )
        return render(request, self.template_name, {'form': form})


class AttendanceMarkView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'attendance/mark_attendance.html'
    permission_required = 'students.add_attendance'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, clas_nm, clas_sec, att_date):
        cls = get_object_or_404(ClassName, pk=clas_nm)
        section = get_object_or_404(SectionClas, pk=clas_sec)
        date = datetime.date.fromisoformat(att_date)
        students = StudentsInfo.objects.filter(
            class_name=cls, section_class=section, is_deleted=False
        ).order_by('unique_roll')
        existing = {
            att.student_id: att.status
            for att in Attendance.objects.filter(
                class_name=cls, section=section, date=date
            )
        }
        object_list = [
            {'student': student, 'status': existing.get(student.id, 'present')}
            for student in students
        ]
        context = {
            'class': cls,
            'section': section,
            'date': date,
            'object_list': object_list,
            'status_choices': STATUS_CHOICES,
        }
        return render(request, self.template_name, context)

    def post(self, request, clas_nm, clas_sec, att_date):
        cls = get_object_or_404(ClassName, pk=clas_nm)
        section = get_object_or_404(SectionClas, pk=clas_sec)
        date = datetime.date.fromisoformat(att_date)
        student_ids = request.POST.getlist('sid')

        saved = 0
        for student_id in student_ids:
            student = get_object_or_404(StudentsInfo, pk=student_id)
            status = request.POST.get(f'status_{student_id}', 'present')
            Attendance.objects.update_or_create(
                student=student, date=date,
                defaults={
                    'class_name': cls,
                    'section': section,
                    'status': status,
                    'marked_by': request.user,
                }
            )
            saved += 1

        messages.success(
            request, f'Attendance saved for {saved} student(s) on {date}.'
        )
        return redirect(
            'students:attendance_mark',
            clas_nm=cls.id, clas_sec=section.id, att_date=date.isoformat()
        )


class AttendanceReportView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'attendance/attendance_report.html'
    permission_required = 'students.view_attendance'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        classes = ClassName.objects.filter(is_active=True)
        sections = SectionClas.objects.filter(is_active=True)
        qs = Attendance.objects.select_related('student', 'class_name', 'section')

        class_id = request.GET.get('class_name')
        section_id = request.GET.get('section')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if class_id:
            qs = qs.filter(class_name_id=class_id)
        if section_id:
            qs = qs.filter(section_id=section_id)
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        summary = {
            'total': qs.count(),
            'present': qs.filter(status='present').count(),
            'absent': qs.filter(status='absent').count(),
            'late': qs.filter(status='late').count(),
            'leave': qs.filter(status='leave').count(),
        }
        records = qs.order_by('-date')[:300]

        context = {
            'classes': classes,
            'sections': sections,
            'records': records,
            'summary': summary,
            'selected_class': class_id,
            'selected_section': section_id,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, self.template_name, context)
