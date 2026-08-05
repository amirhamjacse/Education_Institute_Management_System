import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from institute_dashaboard.models import Teachers_Information, TeacherAttendance


class TeacherAttendanceMarkView(
    LoginRequiredMixin, UserPassesTestMixin, View
):
    template_name = 'teacher_attendance.html'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        date_str = request.GET.get('date') or datetime.date.today().isoformat()
        date = datetime.date.fromisoformat(date_str)
        teachers = Teachers_Information.objects.all().order_by('teachers_name')
        existing = {
            att.teacher_id: att.status
            for att in TeacherAttendance.objects.filter(date=date)
        }
        object_list = [
            {'teacher': teacher, 'status': existing.get(teacher.id, 'present')}
            for teacher in teachers
        ]
        context = {
            'object_list': object_list,
            'date': date,
            'status_choices': TeacherAttendance.STATUS_CHOICES,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        date = datetime.date.fromisoformat(request.POST.get('date'))
        teacher_ids = request.POST.getlist('tid')

        saved = 0
        for teacher_id in teacher_ids:
            teacher = get_object_or_404(Teachers_Information, pk=teacher_id)
            status = request.POST.get(f'status_{teacher_id}', 'present')
            TeacherAttendance.objects.update_or_create(
                teacher=teacher, date=date,
                defaults={'status': status, 'marked_by': request.user}
            )
            saved += 1

        messages.success(
            request, f'Attendance saved for {saved} teacher(s) on {date}.'
        )
        return redirect(f"{request.path}?date={date.isoformat()}")


class TeacherAttendanceReportView(
    LoginRequiredMixin, UserPassesTestMixin, View
):
    template_name = 'teacher_attendance_report.html'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        qs = TeacherAttendance.objects.select_related('teacher')

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
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
            'records': records,
            'summary': summary,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, self.template_name, context)
