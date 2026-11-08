from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView
from students.models import (
    StudentsInfo, Attendance, ResultInfo,
    BookIssue, BedAllocation, StudentTransport, ExamAdmitCard
)
from fees.models import Invoice


class StudentAdminDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    360-degree comprehensive profile of a student for administrators and teachers.
    Aggregates academics, attendance %, invoices & billing, library loans,
    hostel, transport, and exam cards.
    """
    model = StudentsInfo
    template_name = 'studentsinfo/student_admin_detail.html'
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.is_active

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object

        # 1. Billing & Invoices (using properties)
        invoices = list(Invoice.objects.filter(student=student, is_deleted=False).select_related('fee_head').order_by('-id'))
        total_inv = sum((inv.net_amount for inv in invoices), 0)
        total_paid = sum((inv.paid_amount for inv in invoices), 0)
        total_due = sum((inv.due_amount for inv in invoices), 0)

        # 2. Attendance Stats
        attendance_qs = Attendance.objects.filter(student=student).order_by('-date')
        total_days = attendance_qs.count()
        present_days = attendance_qs.filter(status='present').count()
        absent_days = attendance_qs.filter(status='absent').count()
        leave_days = attendance_qs.filter(status='leave').count()
        late_days = attendance_qs.filter(status='late').count()
        attendance_pct = round((present_days / total_days * 100), 1) if total_days > 0 else 0

        # 3. Academic Results
        results = ResultInfo.objects.filter(student=student).select_related(
            'subject', 'exam_type', 'exam_year', 'class_name'
        ).order_by('-id')

        # 4. Library Circulation
        book_issues = BookIssue.objects.filter(student=student).select_related('book').order_by('-issue_date')

        # 5. Campus Operations (Hostel & Transport)
        hostel_bed = BedAllocation.objects.filter(
            student=student, is_active=True
        ).select_related('room', 'room__hostel').first()

        transport_pass = StudentTransport.objects.filter(
            student=student, is_active=True
        ).select_related('route', 'route__vehicle').first()

        # 6. Exam Admit Cards
        admit_cards = ExamAdmitCard.objects.filter(student=student).order_by('-id')

        context.update({
            'invoices': invoices,
            'total_invoiced': total_inv,
            'total_paid': total_paid,
            'total_due': total_due,
            'attendance_records': attendance_qs[:30],
            'total_attendance_days': total_days,
            'present_days': present_days,
            'absent_days': absent_days,
            'leave_days': leave_days,
            'late_days': late_days,
            'attendance_percentage': attendance_pct,
            'results': results,
            'book_issues': book_issues,
            'hostel_bed': hostel_bed,
            'transport_pass': transport_pass,
            'admit_cards': admit_cards,
        })
        return context
