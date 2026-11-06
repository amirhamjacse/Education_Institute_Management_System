from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.db.models import Count, Q

from students.models import (
    StudentsInfo, Attendance, ResultInfo,
    ClassRoutine, TimeSlot
)
from fees.models import Invoice
from institute_dashaboard.models import Web_Heading, Notice_board


class ParentPortalView(View):
    """Parent & Guardian self-service portal to monitor child's academic progress"""
    template_name = 'dashboard/parent_portal.html'

    def _handle_request(self, request, roll_number, phone_number):
        student = None
        attendance_stats = None
        recent_attendance = None
        results = None
        invoices = None
        routines = None

        if roll_number and phone_number:
            student = StudentsInfo.objects.filter(
                unique_roll=roll_number,
                gurdian_mobile_number__icontains=phone_number,
                is_active=True
            ).select_related('class_name', 'section_class').first()

            if student:
                # Attendance calculation
                total_att = Attendance.objects.filter(student=student).count()
                present_att = Attendance.objects.filter(student=student, status='P').count()
                absent_att = Attendance.objects.filter(student=student, status='A').count()
                late_att = Attendance.objects.filter(student=student, status='L').count()
                att_pct = round((present_att / total_att * 100), 1) if total_att > 0 else 100.0

                attendance_stats = {
                    'total': total_att,
                    'present': present_att,
                    'absent': absent_att,
                    'late': late_att,
                    'percentage': att_pct,
                }
                recent_attendance = Attendance.objects.filter(student=student).order_by('-date')[:15]

                # Exam Results
                results = ResultInfo.objects.filter(student=student).select_related('subject', 'exam_type', 'exam_year')

                # Unpaid & Paid Fee Invoices
                invoices = Invoice.objects.filter(student=student).order_by('-due_date')

                # Weekly Class Routine
                routines = ClassRoutine.objects.filter(
                    class_name=student.class_name,
                    section=student.section_class,
                    is_active=True
                ).select_related('subject', 'teacher', 'time_slot').order_by('day_of_week', 'time_slot__start_time')
            else:
                messages.error(request, 'No active student found matching that Roll Number and Guardian Phone Number.')

        webheading = Web_Heading.objects.last()
        notices = Notice_board.objects.all().order_by('-id')[:5]

        return render(request, self.template_name, {
            'student': student,
            'attendance_stats': attendance_stats,
            'recent_attendance': recent_attendance,
            'results': results,
            'invoices': invoices,
            'routines': routines,
            'roll_number': roll_number,
            'phone_number': phone_number,
            'webname': webheading,
            'notices': notices,
        })

    def get(self, request, *args, **kwargs):
        roll = request.GET.get('roll', '').strip()
        phone = request.GET.get('phone', '').strip()
        return self._handle_request(request, roll, phone)

    def post(self, request, *args, **kwargs):
        roll = request.POST.get('roll', '').strip()
        phone = request.POST.get('phone', '').strip()
        return self._handle_request(request, roll, phone)
