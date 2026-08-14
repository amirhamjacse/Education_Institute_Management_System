from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View

from fees.models import Invoice, INVOICE_STATUS
from students.models.class_studn import ClassName, SectionClas


class InvoiceListView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/invoice_list.html'
    permission_required = 'fees.view_invoice'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        qs = Invoice.objects.filter(is_deleted=False).select_related(
            'student', 'class_name', 'section', 'fee_head'
        )

        search = request.GET.get('q')
        class_id = request.GET.get('class_name')
        section_id = request.GET.get('section')
        session = request.GET.get('session')
        status = request.GET.get('status')

        if search:
            qs = qs.filter(
                Q(student__name__icontains=search)
                | Q(student__unique_roll__icontains=search)
                | Q(invoice_no__icontains=search)
            )
        if class_id:
            qs = qs.filter(class_name_id=class_id)
        if section_id:
            qs = qs.filter(section_id=section_id)
        if session:
            qs = qs.filter(session=session)
        if status:
            qs = qs.filter(status=status)

        paginator = Paginator(qs, 50)
        page_obj = paginator.get_page(request.GET.get('page'))

        context = {
            'page_obj': page_obj,
            'classes': ClassName.objects.filter(is_active=True),
            'sections': SectionClas.objects.filter(is_active=True),
            'status_choices': INVOICE_STATUS,
            'search': search or '',
            'selected_class': class_id,
            'selected_section': section_id,
            'selected_session': session,
            'selected_status': status,
        }
        return render(request, self.template_name, context)
