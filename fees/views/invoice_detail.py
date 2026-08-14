from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from fees.forms import PaymentForm
from fees.models import Invoice, Payment


class InvoiceDetailView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/invoice_detail.html'
    permission_required = 'fees.view_invoice'

    def test_func(self):
        return self.request.user.is_active

    def _context(self, request, pk, payment_form=None):
        invoice = get_object_or_404(
            Invoice.objects.select_related('student', 'class_name', 'section', 'fee_head'),
            pk=pk
        )
        # Self-heal a stale unpaid->overdue status whenever someone looks at it,
        # since there's no scheduler in this project to do it automatically.
        invoice.recompute_status()
        payments = invoice.payments.exclude(is_deleted=True).order_by('-paid_on', '-created_time')
        can_record_payment = (
            invoice.status not in ('paid', 'cancelled')
            and request.user.has_perm('fees.add_payment')
        )
        return {
            'invoice': invoice,
            'payments': payments,
            'payment_form': payment_form or PaymentForm(),
            'can_record_payment': can_record_payment,
            'can_void_payment': request.user.has_perm('fees.delete_payment'),
        }

    def get(self, request, pk):
        return render(request, self.template_name, self._context(request, pk))

    def post(self, request, pk):
        action = request.POST.get('action')
        if action == 'void_payment':
            return self._void_payment(request, pk)
        return self._record_payment(request, pk)

    def _record_payment(self, request, pk):
        if not request.user.has_perm('fees.add_payment'):
            messages.error(request, "You don't have permission to record payments.")
            return redirect('fees:invoice_detail', pk=pk)

        form = PaymentForm(request.POST)
        with transaction.atomic():
            invoice = get_object_or_404(Invoice.objects.select_for_update(), pk=pk)
            if invoice.status in ('paid', 'cancelled'):
                messages.error(request, 'This invoice cannot accept further payments.')
                return redirect('fees:invoice_detail', pk=pk)
            if not form.is_valid():
                return render(request, self.template_name, self._context(request, pk, payment_form=form))

            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.received_by = request.user
            if payment.amount > invoice.due_amount > 0:
                messages.warning(
                    request,
                    f'Payment of {payment.amount} exceeds the due amount of '
                    f'{invoice.due_amount} — recorded as an overpayment.'
                )
            payment.save()
            invoice.recompute_status()

        messages.success(request, f'Payment {payment.receipt_no} recorded.')
        return redirect('fees:invoice_detail', pk=pk)

    def _void_payment(self, request, pk):
        if not request.user.has_perm('fees.delete_payment'):
            messages.error(request, "You don't have permission to void payments.")
            return redirect('fees:invoice_detail', pk=pk)

        payment_id = request.POST.get('payment_id')
        with transaction.atomic():
            invoice = get_object_or_404(Invoice.objects.select_for_update(), pk=pk)
            payment = get_object_or_404(Payment, pk=payment_id, invoice=invoice)
            payment.soft_delete()
            invoice.recompute_status()

        messages.success(request, f'Payment {payment.receipt_no} voided.')
        return redirect('fees:invoice_detail', pk=pk)


class InvoiceReceiptPrintView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/invoice_receipt_print.html'
    permission_required = 'fees.view_invoice'

    def test_func(self):
        return self.request.user.is_active

    def has_permission(self):
        # Staff with fees.view_invoice can print any receipt; a student can
        # only print their own, without needing that blanket permission.
        if super().has_permission():
            return True
        student_profile = getattr(self.request.user, 'student_profile', None)
        if student_profile is None:
            return False
        return Invoice.objects.filter(
            pk=self.kwargs.get('pk'), student=student_profile
        ).exists()

    def get(self, request, pk):
        invoice = get_object_or_404(
            Invoice.objects.select_related('student', 'class_name', 'section', 'fee_head'),
            pk=pk
        )
        payments = invoice.payments.exclude(is_deleted=True).order_by('paid_on')
        return render(
            request, self.template_name,
            {'invoice': invoice, 'payments': payments}
        )
