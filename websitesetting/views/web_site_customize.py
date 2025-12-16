from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, View
)
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin
)
from students.models.students_info import StudentsInfo
from students.forms.studentscreateform import StudentsInfoForm
from students.forms.result_input import ResultInputForm
from institute_dashaboard.models import Web_Heading

class WebHeadinView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    model = Web_Heading
    permission_required = 'institute_dashaboard.add_web_heading'
    template_name = 'webs/heading_add.html'

    def test_func(self):
        return self.request.user.is_active
    
    def get(self, request):
        stdn = 'h'
        form = 'form'
        context = {
            'object_list': stdn,
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = ResultInputForm(request.POST)
        markes = []
        for mark in request.POST.getlist('mark'):
            markes.append(mark)
        i=0
        for single_mark in markes:
            for student in request.POST.getlist('sid'):
                students = StudentsInfo.objects.get(id=student)
                a = markes[i]
                i += 1
                print(a, '----')
                print(students, 'ddd---dd')
                
                # V_insert_data.save()
        #             if form.is_valid():
        #     print('d')
        # else:
                # V_insert_data = studentsEnrolledSubjectsGrade(
                # Teacher=teacher,
                # Students_Enrollment_Records=students,
                # Date=single_date,
                # Grade=markes[i]
                # )
        #     print('error')
        return render(request, self.template_name)