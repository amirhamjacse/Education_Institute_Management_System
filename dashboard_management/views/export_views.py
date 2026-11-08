import csv
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from students.models import StudentsInfo
from fees.models import Invoice


class ExportStudentsCSVView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Exports active student directory to CSV for administrative records and reporting."""
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="students_roster_{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Roll No', 'Full Name', 'Class', 'Section', 'Session', 'Gender', 'Blood Group', 'Father Name', 'Guardian Phone', 'Admission Date'])

        students = StudentsInfo.objects.select_related('class_name', 'section_class').order_by('class_name__name', 'unique_roll')
        for s in students:
            writer.writerow([
                s.unique_roll or '',
                s.name or '',
                s.class_name.name if s.class_name else '',
                s.section_class.name if s.section_class else '',
                s.session or '',
                s.gender or '',
                s.blood_group or '',
                s.father_name or '',
                s.gurdian_mobile_number or '',
                s.admission_date or '',
            ])

        return response


class ExportInvoicesCSVView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Exports fee invoice records to CSV."""
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="fee_invoices_{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Invoice No', 'Student Name', 'Roll No', 'Class', 'Fee Head', 'Session', 'Amount', 'Status', 'Date'])

        invoices = Invoice.objects.select_related('student', 'class_name', 'fee_head').order_by('-id')
        for inv in invoices:
            writer.writerow([
                inv.invoice_no or '',
                inv.student.name if inv.student else '',
                inv.student.unique_roll if inv.student else '',
                inv.class_name.name if inv.class_name else '',
                inv.fee_head.name if inv.fee_head else '',
                inv.session or '',
                inv.amount or 0,
                inv.status or '',
                inv.created_time.strftime('%Y-%m-%d') if hasattr(inv, 'created_time') and inv.created_time else '',
            ])

        return response
