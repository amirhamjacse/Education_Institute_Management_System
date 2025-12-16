from django.shortcuts import render
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, TemplateView, View
)
from students.models import StudentsInfo
from institute_dashaboard.models import OnlineAdmission, complain
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin
)


class OnlineAdmissionProcess(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    model = OnlineAdmission
    template_name = 'online_admission.html'
    permission_required = 'dashboard_management.view_students'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, *args, **kwargs):
        online_admission_apply_count = OnlineAdmission.objects.filter(
            is_active=True
        )
        context = {
            'online_admission_apply':online_admission_apply_count,
        }
        return render(request, self.template_name, context)