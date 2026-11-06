from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from fees.models import Invoice, Payment
from institute_dashaboard.views import sslcommerz_payment_gateway


class PayOnlineInvoiceView(LoginRequiredMixin, View):
    """Initiates SSLCommerz online payment for a student's invoice"""

    def get(self, request, pk, *args, **kwargs):
        invoice = get_object_or_404(Invoice, pk=pk, is_deleted=False)

        # Allow student owner or staff
        if hasattr(request.user, 'student_profile'):
            if invoice.student != request.user.student_profile:
                messages.error(request, 'You cannot pay another student\'s invoice.')
                return redirect('fees:my_invoices')

        if invoice.status == 'PAID':
            messages.info(request, 'This invoice is already marked as paid.')
            return redirect('fees:my_invoices' if hasattr(request.user, 'student_profile') else 'fees:invoice_detail', pk=pk)

        due_amount = invoice.due_amount
        name = f"Invoice {invoice.invoice_no} - {invoice.student.name}"

        # Initialize SSLCommerz gateway
        gateway_url = sslcommerz_payment_gateway(request, name, due_amount)
        if gateway_url:
            return redirect(gateway_url)

        messages.error(request, 'Unable to initiate online payment session. Please try again or pay at the cash counter.')
        return redirect('fees:invoice_detail', pk=pk)
