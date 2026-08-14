from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View

from fees.forms import FeeStructureForm
from fees.models import FeeStructure
from students.models.class_studn import ClassName


class FeeStructureListView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/fee_structure_list.html'
    permission_required = 'fees.view_feestructure'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        qs = FeeStructure.objects.filter(is_deleted=False).select_related(
            'fee_head', 'class_name'
        )
        class_id = request.GET.get('class_name')
        session = request.GET.get('session')
        if class_id:
            qs = qs.filter(class_name_id=class_id)
        if session:
            qs = qs.filter(session=session)
        context = {
            'structures': qs,
            'classes': ClassName.objects.filter(is_active=True),
            'selected_class': class_id,
            'selected_session': session,
        }
        return render(request, self.template_name, context)


class FeeStructureCreateView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/fee_structure_form.html'
    permission_required = 'fees.add_feestructure'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        form = FeeStructureForm()
        return render(request, self.template_name, {'form': form, 'is_edit': False})

    def post(self, request):
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure added.')
            return redirect('fees:fee_structure_list')
        return render(request, self.template_name, {'form': form, 'is_edit': False})


class FeeStructureUpdateView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'fees/fee_structure_form.html'
    permission_required = 'fees.change_feestructure'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, pk):
        structure = get_object_or_404(FeeStructure, pk=pk)
        form = FeeStructureForm(instance=structure)
        return render(request, self.template_name, {'form': form, 'is_edit': True})

    def post(self, request, pk):
        structure = get_object_or_404(FeeStructure, pk=pk)
        form = FeeStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee structure updated.')
            return redirect('fees:fee_structure_list')
        return render(request, self.template_name, {'form': form, 'is_edit': True})
