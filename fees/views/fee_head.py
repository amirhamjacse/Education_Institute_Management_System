from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.shortcuts import redirect, render
from django.views.generic import View

from fees.forms import FeeHeadForm
from fees.models import FeeHead


class FeeHeadListView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/fee_head_list.html'
    permission_required = 'fees.view_feehead'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        fee_heads = FeeHead.objects.filter(is_deleted=False)
        form = FeeHeadForm()
        return render(
            request, self.template_name,
            {'fee_heads': fee_heads, 'form': form}
        )

    def post(self, request):
        if not request.user.has_perm('fees.add_feehead'):
            messages.error(request, "You don't have permission to add fee heads.")
            return redirect('fees:fee_head_list')
        form = FeeHeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee head added.')
            return redirect('fees:fee_head_list')
        fee_heads = FeeHead.objects.filter(is_deleted=False)
        return render(
            request, self.template_name,
            {'fee_heads': fee_heads, 'form': form}
        )
