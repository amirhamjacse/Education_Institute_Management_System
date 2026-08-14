import datetime

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View

from fees.forms import InvoiceGenerateQueryForm, AdHocInvoiceForm
from fees.models import FeeStructure, Invoice
from students.models.class_studn import ClassName, SectionClas
from students.models.students_info import StudentsInfo

# SectionClas primary keys are positive autoincrement ids, so 0 is used as
# a sentinel in the URL to mean "no section filter — all sections".
NO_SECTION = 0


class InvoiceGenerateQueryView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/invoice_generate_query.html'
    permission_required = 'fees.add_invoice'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        form = InvoiceGenerateQueryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InvoiceGenerateQueryForm(request.POST)
        if form.is_valid():
            cls = form.cleaned_data['class_name']
            section = form.cleaned_data['section']
            fee_structure = form.cleaned_data['fee_structure']
            period = form.cleaned_data['period_label'] or 'one-time'
            due_date = form.cleaned_data['due_date']
            return redirect(
                'fees:invoice_generate_bulk',
                cls=cls.id, sec=section.id if section else NO_SECTION,
                fs=fee_structure.id, period=period,
                due_date=due_date.isoformat()
            )
        return render(request, self.template_name, {'form': form})


class InvoiceGenerateBulkView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/invoice_generate_bulk.html'
    permission_required = 'fees.add_invoice'

    def test_func(self):
        return self.request.user.is_active

    def _context(self, request, cls, sec, fs, period, due_date):
        cls_obj = get_object_or_404(ClassName, pk=cls)
        section_obj = get_object_or_404(SectionClas, pk=sec) if sec != NO_SECTION else None
        fee_structure = get_object_or_404(FeeStructure, pk=fs)
        due_date_obj = datetime.date.fromisoformat(due_date)

        students = StudentsInfo.objects.filter(
            class_name=cls_obj, session=fee_structure.session, is_deleted=False
        )
        if section_obj:
            students = students.filter(section_class=section_obj)
        students = students.order_by('unique_roll')

        already_invoiced = set(
            Invoice.objects.filter(
                fee_structure=fee_structure, period_label=period,
                student__in=students
            ).values_list('student_id', flat=True)
        )

        object_list = [
            {'student': student, 'already_invoiced': student.id in already_invoiced}
            for student in students
        ]
        return {
            'class': cls_obj,
            'section': section_obj,
            'fee_structure': fee_structure,
            'period': period,
            'due_date': due_date_obj,
            'object_list': object_list,
            'cls': cls, 'sec': sec, 'fs': fs,
        }

    def get(self, request, cls, sec, fs, period, due_date):
        context = self._context(request, cls, sec, fs, period, due_date)
        return render(request, self.template_name, context)

    def post(self, request, cls, sec, fs, period, due_date):
        context = self._context(request, cls, sec, fs, period, due_date)
        fee_structure = context['fee_structure']
        due_date_obj = context['due_date']
        section_obj = context['section']
        cls_obj = context['class']

        student_ids = request.POST.getlist('sid')
        created = 0
        skipped = 0
        for row in context['object_list']:
            student = row['student']
            # Already-invoiced rows render as disabled+unchecked, so a
            # browser resubmit never includes their id — check this first
            # so re-generating still reports them as skipped, not ignored.
            if row['already_invoiced']:
                skipped += 1
                continue
            if str(student.id) not in student_ids:
                continue
            Invoice.objects.create(
                student=student,
                class_name=cls_obj,
                section=student.section_class or section_obj,
                fee_structure=fee_structure,
                fee_head=fee_structure.fee_head,
                session=fee_structure.session,
                period_label=period,
                amount=fee_structure.amount,
                due_date=due_date_obj,
                generated_by=request.user,
            )
            created += 1

        messages.success(
            request,
            f'{created} invoice(s) created, {skipped} skipped (already invoiced).'
        )
        return redirect(
            'fees:invoice_generate_bulk',
            cls=cls, sec=sec, fs=fs, period=period, due_date=due_date
        )


class AdHocInvoiceCreateView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/invoice_adhoc_form.html'
    permission_required = 'fees.add_invoice'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        form = AdHocInvoiceForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AdHocInvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            student = invoice.student
            invoice.class_name = student.class_name
            invoice.section = student.section_class
            invoice.session = student.session or ''
            invoice.fee_structure = None
            invoice.generated_by = request.user
            invoice.save()
            messages.success(request, f'Invoice {invoice.invoice_no} created.')
            return redirect('fees:invoice_detail', pk=invoice.pk)
        return render(request, self.template_name, {'form': form})
