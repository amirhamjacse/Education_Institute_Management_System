from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, View
)
from django.contrib import messages

from django.shortcuts import get_object_or_404, render, redirect
# from utils import render_pdf
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin
)
from students.models.students_info import StudentsInfo
from students.models.subject import Subjects
from students.models.class_studn import ClassName, ClassYear, SectionClas

from students.models.result import ResultInfo, Exam, ExamYear
from students.forms.result_input import ResultInputForm, AddResultstdlist, ClasYearForm


class ResultsCreateView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, CreateView
):

    model = ResultInfo
    template_name = 'result/result_input.html'
    permission_required = 'students.add_resultinfo'
    form_class = ResultInputForm
    success_url = reverse_lazy('students:students_list')

    def test_func(self):
        return self.request.user.is_active

    def get_context_data(self, **kwargs):
        objects = self.kwargs['stdn']
        sub_pk = self.kwargs['subj']
        students = StudentsInfo.objects.filter(id=objects)
        students = get_object_or_404(StudentsInfo, pk=objects)
        subject = get_object_or_404(Subjects, pk=sub_pk)
        # print( students.section_class, print('--=-=-'))
        kwargs['name'] = students.name
        kwargs['class'] = students.class_name
        kwargs['section'] = students.section_class
        kwargs['roll'] = students.unique_roll
        kwargs['sub'] = subject
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form, **kwargs):
        objects = self.kwargs['stdn']
        sub_pk = self.kwargs['subj']
        students = get_object_or_404(StudentsInfo, pk=objects)
        subject = get_object_or_404(Subjects, pk=sub_pk)
        # print(objects, subject.name.pk, students.class_name, print('--=-=-'))
        # print(form)
        insta = form.save(commit=False)
        insta.class_name = students.class_name
        insta.section = students.section_class
        insta.subject = subject
        insta.student = students
        insta.save()
        return super().form_valid(form)


class ListOfResultsAddView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):

    model = ResultInfo
    template_name = 'result/query_for_add_result.html'
    permission_required = 'students.add_resultinfo'
    form_class = AddResultstdlist
    # success_url = reverse_lazy('students:students_list')

    def test_func(self):
        return self.request.user.is_active
    
    def get(self, request):
        form = self.form_class
        forms = ClasYearForm()
        context= {
            'form': form,
            'forms': forms
        }
        return render(request, self.template_name, context)


    def post(self, request):
        # form = AddResultstdlist(request.POST)
        # if form.is_valid():
        #     form.save()
        cls_id = request.POST.get('class_name')
        clsyr_id = request.POST.get('class_nm')
        sec_id = request.POST.get('section')
        sub_id = request.POST.get('subject')
        exmtyp_id = request.POST.get('exam_type')
        emyr_id = request.POST.get('exam_year')
        cls = get_object_or_404(ClassName, pk=cls_id)
        clsyear = get_object_or_404(ClassYear, pk=clsyr_id)
        section = get_object_or_404(SectionClas, pk=sec_id)
        subject = get_object_or_404(Subjects, pk=sub_id)
        exmtype = get_object_or_404(Exam, pk=exmtyp_id)
        exmyr = get_object_or_404(ExamYear, pk=emyr_id)
        # std_list = StudentsInfo.objects.filter(
        #     class_name=cls, section_class=section
        # )
        # print(std_list)
        # markes = []
        # for mark in request.POST.getlist('mark'):
        #     markes.append(mark)
        # print(markes)
        context = {
            'class': cls,
            'class_year': clsyear,
            'section': section,
            'subject': subject,
            'exmtype': exmtype,
            'exmyr': exmyr

        }
        return render(request, 'result/make_sure_add_result.html', context)


class ListOfResultscCeateResultView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    model = ResultInfo
    template_name = 'result/add_result_list.html'
    permission_required = 'students.add_resultinfo'
    form_class = AddResultstdlist

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, clas_nm, clas_yr, clas_sec, exm_tp, sub, ecm_yr):
        cls = get_object_or_404(ClassName, pk=clas_nm)
        clsyear = get_object_or_404(ClassYear, pk=clas_yr)
        section = get_object_or_404(SectionClas, pk=clas_sec)
        # subject = get_object_or_404(Subjects, pk=sub_id)
        # exmtype = get_object_or_404(Exam, pk=exmtyp_id)
        # exmyr = get_object_or_404(ExamYear, pk=emyr_id)
        std_list = StudentsInfo.objects.select_related().filter(
            class_name=cls, section_class=section, class_name__class_nm=clsyear.id
        )
        context= {
            'object_list': std_list,
        }
        return render(request, self.template_name, context)
    

    def post(self, request, clas_nm, clas_yr, clas_sec, exm_tp, sub, ecm_yr):
        cls = get_object_or_404(ClassName, pk=clas_nm)
        section = get_object_or_404(SectionClas, pk=clas_sec)
        subject = get_object_or_404(Subjects, pk=sub)
        exmtype = get_object_or_404(Exam, pk=exm_tp)
        exmyr = get_object_or_404(ExamYear, pk=ecm_yr)
        
        marks = request.POST.getlist('mark')  # Get all marks at once
        student_ids = request.POST.getlist('sid')  # Get all student IDs at once

        # Ensure the number of marks matches the number of students
        if len(marks) != len(student_ids):
            # Handle error: Number of marks and students do not match
            return render(request, self.template_name, {'error': 'Number of marks and students do not match.'})

        for i, student_id in enumerate(student_ids):
            students = get_object_or_404(StudentsInfo, id=student_id)  # Safely get student
            reg = ResultInfo(
                class_name=cls,
                subject=subject,
                section=section,
                exam_type=exmtype,
                exam_year=exmyr,
                student=students,
                marks=marks[i]  # Use indexed marks
            )
            reg.save()
        messages.success(request, 'Results uploaded successfully!')
        return redirect('students:students_list_for_result')  # Redirect after processing all students


    # def post(self, request, clas_nm, clas_yr, clas_sec,  exm_tp, sub, ecm_yr):
    #     # print(cls, 'cls')
    #     # clsyear = get_object_or_404(ClassYear, pk=clas_yr)
    #     cls = get_object_or_404(ClassName, pk=clas_nm)
    #     section = get_object_or_404(SectionClas, pk=clas_sec)
    #     subject = get_object_or_404(Subjects, pk=sub)
    #     exmtype = get_object_or_404(Exam, pk=exm_tp)
    #     exmyr = get_object_or_404(ExamYear, pk=ecm_yr)
    #     markes = []
    #     for mark in request.POST.getlist('mark'):
    #         markes.append(mark)
    #     i=0
    #     for single_mark in markes:
    #         for student in request.POST.getlist('sid'):
    #             students = StudentsInfo.objects.get(id=student)
    #             reg = ResultInfo(
    #                 class_name =cls,
    #                 subject=subject,
    #                 section=section,
    #                 exam_type=exmtype,
    #                 exam_year=exmyr,
    #                 student=students,
    #                 marks = markes[i]
    #             )
    #             reg.save()
    #             i += 1
    #             return redirect('students:show_result')
    #         return render(request, self.template_name)


class ShowResultView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    model = StudentsInfo
    template_name = 'result/show_result_list.html'
    permission_required = 'students.add_resultinfo'
    form_class = AddResultstdlist

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        std_list = StudentsInfo.objects.all()
        context = {
            'object_list': std_list
        }
        return render(request, self.template_name, context)

class SemesterResultView(
      LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, DetailView
):
    model = StudentsInfo
    template_name = 'result/result_details.html'
    permission_required = 'students.add_resultinfo'

    def test_func(self):
        return self.request.user.is_active

    def get_context_data(self, **kwargs):
        sem = self.kwargs['sem']
        stdn_obj = self.get_object()
        exmtype = get_object_or_404(Exam, pk=1)
        # print(exmtype.exams.subject)
        exmtyped = get_object_or_404(Exam, pk=2)
        rslt = ResultInfo.objects.filter(student=stdn_obj, )
        rslt_inf = ResultInfo.objects.filter(student=stdn_obj, exam_type=exmtype).last()
        sems = ResultInfo.objects.filter(student=stdn_obj, exam_type=exmtyped).last()
        print(rslt)
        kwargs['result'] = rslt
        kwargs['rslt_inf'] = rslt_inf
        kwargs['sems'] = sems
        return super().get_context_data(**kwargs)

class SemesterResultViews(View):
    # def get(self, request, sem, pk):
    #     # sem = self.kwargs['sem']
    #     # sems
    #     stdn_obj = get_object_or_404(StudentsInfo, pk=pk)

    #     print(stdn_obj)
    #     exmtype = get_object_or_404(Exam, pk=1)
    #     # print(exmtype.exams.subject)
    #     exmtyped = get_object_or_404(Exam, pk=2)
    #     rslt = ResultInfo.objects.filter(student=stdn_obj, )
    #     rslt_inf = ResultInfo.objects.filter(student=stdn_obj, exam_type=exmtype).last()
    #     sems = ResultInfo.objects.filter(student=stdn_obj, exam_type=exmtyped).last()
    #     context = {
    #         'result' : rslt,
    #         'rslt_inf': rslt_inf,
    #         'sems' : sems
    #     }
    #     pdf = RenderPdf('result/a.html', context)
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     filename = "result%s.pdf" %(date.today())
    #     content = "attachment; filename=%s" %(filename)
    #     response['Content-Disposition'] = content
    #     return response
    
    def get(self, request, sem, pk):
        stdn_obj = get_object_or_404(StudentsInfo, pk=pk)

        print(stdn_obj)
        exmtype = get_object_or_404(Exam, pk=1)
        # print(exmtype.exams.subject)
        exmtyped = get_object_or_404(Exam, pk=2)
        rslt = ResultInfo.objects.filter(student=stdn_obj, )
        rslt_inf = ResultInfo.objects.filter(student=stdn_obj, exam_type=exmtype).last()
        sems = ResultInfo.objects.filter(student=stdn_obj, exam_type=exmtyped).last()
        context = {
            'result' : rslt,
            'rslt_inf': rslt_inf,
            'sems' : sems

        }
        return render_pdf(
        request=request,
        template='result/a.html',
        context=context,
        file_name='reportcard.pdf'
    )