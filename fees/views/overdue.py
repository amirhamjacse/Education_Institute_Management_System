import datetime

from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.shortcuts import render
from django.views.generic import View

from fees.models import Invoice
from students.models.class_studn import ClassName, SectionClas


class OverdueInvoiceListView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/overdue_invoices.html'
    permission_required = 'fees.view_invoice'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        today = datetime.date.today()
        qs = Invoice.objects.filter(
            is_deleted=False, status__in=['unpaid', 'partial'],
            due_date__lt=today
        ).select_related('student', 'class_name', 'section', 'fee_head')

        class_id = request.GET.get('class_name')
        section_id = request.GET.get('section')
        if class_id:
            qs = qs.filter(class_name_id=class_id)
        if section_id:
            qs = qs.filter(section_id=section_id)

        qs = qs.order_by('due_date')
        rows = [
            {'invoice': invoice, 'days_overdue': (today - invoice.due_date).days}
            for invoice in qs[:300]
        ]

        context = {
            'rows': rows,
            'classes': ClassName.objects.filter(is_active=True),
            'sections': SectionClas.objects.filter(is_active=True),
            'selected_class': class_id,
            'selected_section': section_id,
        }
        return render(request, self.template_name, context)
