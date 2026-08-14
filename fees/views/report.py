from decimal import Decimal

from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.db.models import Sum, F
from django.shortcuts import render
from django.views.generic import View

from fees.models import Invoice, Payment
from students.models.class_studn import ClassName


class FeeCollectionReportView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/fee_report.html'
    permission_required = 'fees.view_invoice'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        invoices = Invoice.objects.filter(is_deleted=False)
        payments = Payment.objects.filter(is_deleted=False)

        class_id = request.GET.get('class_name')
        session = request.GET.get('session')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if class_id:
            invoices = invoices.filter(class_name_id=class_id)
            payments = payments.filter(invoice__class_name_id=class_id)
        if session:
            invoices = invoices.filter(session=session)
            payments = payments.filter(invoice__session=session)
        if start_date:
            invoices = invoices.filter(due_date__gte=start_date)
            payments = payments.filter(paid_on__gte=start_date)
        if end_date:
            invoices = invoices.filter(due_date__lte=end_date)
            payments = payments.filter(paid_on__lte=end_date)

        total_invoiced = invoices.aggregate(
            total=Sum(F('amount') - F('discount'))
        )['total'] or Decimal('0')
        total_collected = payments.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        total_due = total_invoiced - total_collected

        by_class = invoices.values('class_name__name').annotate(
            invoiced=Sum(F('amount') - F('discount'))
        ).order_by('class_name__name')

        context = {
            'total_invoiced': total_invoiced,
            'total_collected': total_collected,
            'total_due': total_due,
            'by_class': by_class,
            'classes': ClassName.objects.filter(is_active=True),
            'selected_class': class_id,
            'selected_session': session,
            'start_date': start_date or '',
            'end_date': end_date or '',
        }
        return render(request, self.template_name, context)
