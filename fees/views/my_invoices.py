from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import View

from fees.models import Invoice


class MyInvoicesView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Self-service view: a student's own invoices only.

    Ownership-gated (linked student_profile), not permission-gated —
    students are never granted fees.view_invoice, since that would let
    them browse every student's invoices, not just their own.
    """
    template_name = 'fees/my_invoices.html'

    def test_func(self):
        user = self.request.user
        return user.is_active and (user.is_superuser or hasattr(user, 'student_profile'))

    def get(self, request):
        profile = getattr(request.user, 'student_profile', None)
        if profile:
            invoices = Invoice.objects.filter(
                student=profile, is_deleted=False
            ).select_related('fee_head').order_by('-created_time')
        else:
            invoices = []
        return render(request, self.template_name, {'invoices': invoices})
