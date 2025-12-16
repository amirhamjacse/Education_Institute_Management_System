from django.shortcuts import render
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, TemplateView
)
from students.models import StudentsInfo
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin
)



class SDashboard(
    LoginRequiredMixin, UserPassesTestMixin,
    # PermissionRequiredMixin, 
    TemplateView
):
    template_name = 'studentsinfo/dashobard.html'
    # permission_required = 'students.view_students'

    def test_func(self):
        return self.request.user.is_active
    

class StudentsInfoDashboard(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, TemplateView
):
    template_name = 'studentsinfo/stdn_info_dashboard.html'
    permission_required = 'students.view_students'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, *args, **kwargs):
        students_count = StudentsInfo.objects.values_list('id').count()
        # print(students_count, 'total studernts------------------------')
        context = {
            'total_students_count':students_count,
        }
        return self.render_to_response(context)


class ResultsDashboard(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, TemplateView
):
    template_name = 'result/result_dashboard.html'
    permission_required = 'students.view_students'

    def test_func(self):
        return self.request.user.is_active


class StudentsDashboard(
    LoginRequiredMixin, UserPassesTestMixin,
    # PermissionRequiredMixin, 
    TemplateView
):
    template_name = 'studentsinfo/students_dashboard.html'
    permission_required = 'students.view_students'

    def test_func(self):
        return self.request.user.is_active
