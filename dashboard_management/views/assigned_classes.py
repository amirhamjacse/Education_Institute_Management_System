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


class AssignClassesToTeacher(
    LoginRequiredMixin, UserPassesTestMixin,
    # PermissionRequiredMixin, 
    TemplateView
):
    template_name = 'assigned_class.html'
    # permission_required = 'dashboard_management.view_dashboard_management'

    def test_func(self):
        return self.request.user.is_active
