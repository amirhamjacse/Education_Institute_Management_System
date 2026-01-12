from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, View
)
from django.shortcuts import get_object_or_404, render, redirect
# from utils import render_pdf
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin
)
from django.contrib import messages

from students.models.students_info import StudentsInfo
from students.models.subject import Subjects
from students.models.class_studn import ClassName, ClassYear, SectionClas
from students.models.result import ResultInfo, Exam, ExamYear
from students.forms.result_input import ResultInputForm, AddResultstdlist, ClasYearForm


class StudentsSubjects(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    model = StudentsInfo
    template_name = 'dashboard/students_subjects.html'
    permission_required = 'students.add_resultinfo'
    # form_class = AddResultstdlist

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, *args, **kwargs):
        students_id = self.kwargs['stu_id']
        std_instance = StudentsInfo.objects.filter(id=students_id).first()
        class_nms = std_instance.class_name
        print(type(class_nms), class_nms.id, 'class')
        subjects_obj = Subjects.objects.filter(class_nm_id=class_nms.id)
        print(subjects_obj, 'objs subjs')
        context = {
            'students_instance': std_instance,
            'subjects_obj':subjects_obj
        }
        return render(request, self.template_name, context)
    

class StudentsRoutine(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    model = StudentsInfo
    template_name = 'dashboard/students_routine.html'
    permission_required = 'students.add_resultinfo'
    # form_class = AddResultstdlist

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        std_list = StudentsInfo.objects.all()
        context = {
            'object_list': std_list
        }
        return render(request, self.template_name, context)


class StudentsClassRegister(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    model = StudentsInfo
    template_name = 'dashboard/register_new_class.html'
    permission_required = 'students.add_resultinfo'
    # form_class = AddResultstdlist

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, *args, **kwargs):
        students_id = self.kwargs['stu_id']
        students_info = StudentsInfo.objects.filter(id=students_id).first()
        class_nm = ClassName.objects.all()
        section = SectionClas.objects.all()
        context = {
            'object': students_info,
            'class': class_nm,
            'section': section,
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        students_id = self.kwargs['stu_id']
        students_info = StudentsInfo.objects.filter(id=students_id).first()
        selected_class_id = request.POST.get('class_nm')
        selected_section_id = request.POST.get('section')
        class_nm = ClassName.objects.filter(id=selected_class_id).first()
        section = SectionClas.objects.filter(id=selected_section_id).first()
        students_info.class_name = class_nm
        students_info.section_class = section
        students_info.save()
        messages.success(request, 'Registered New class successfully!')
        # have to make a copy of existing object and is_active false for history
        context = {
            'object': students_info,
            # 'class': class_nm,
            # 'section': section,
        }
        return render(request, self.template_name, context)
from decimal import Decimal

class StudentsResultSpecific(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    model = StudentsInfo
    template_name = 'dashboard/students_result.html'
    permission_required = 'students.view_resultinfo'
    # form_class = AddResultstdlist

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        std_list = StudentsInfo.objects.all()
        session = ClassYear.objects.all()
        class_nm = ClassName.objects.all()
        section = SectionClas.objects.all()
        exam = Exam.objects.all()
        exm_year = ExamYear.objects.all()
        context = {
            'object_list': std_list,
            'classes': class_nm,
            'session':session,
            'section':section,
            'exam_nm':exam,
            'exm_years':exm_year,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        selected_class_id = request.POST.get('class_nm')
        selected_session_id = request.POST.get('session')
        selected_exam_year_id = request.POST.get('exam_year')
        selected_exam_type_id = request.POST.get('exam_type')
        unique_id = request.POST.get('unique_id')
        session = ClassYear.objects.filter(id=selected_session_id).last()
        class_nm = ClassName.objects.filter(id=selected_class_id).last()
        # section = SectionClas.objects.all().last()
        exam = Exam.objects.filter(id=selected_exam_type_id).last()
        exm_year = ExamYear.objects.filter(id=selected_exam_year_id).last()
        result = ResultInfo.objects.filter(
            class_name = class_nm,
            # section = section,
            exam_type = exam,
            exam_year = exm_year,
            student__unique_roll = unique_id
        )
        infos = ResultInfo.objects.filter(
            class_name = class_nm,
            # section = section,
            exam_type = exam,
            exam_year = exm_year,
            student__unique_roll = unique_id
        ).last()
        # print(result, 'results')
        result_dict = {}

        for obj in result:
            sub = obj.subject.name
            marks = obj.marks
            
            # Convert marks to float if it's a Decimal
            if isinstance(marks, Decimal):
                marks = float(marks)

            result_dict[sub] = marks

        # Now result_dict will have subjects as keys and marks as values
        # print(result_dict)
    
        # import os
        # import google.generativeai as genai
        # import json

        # # Configure API key from environment variable
        # api_key = "AIzaSyB0l6UWfcqQ5fHDhpYTA_LK0EL0_gKQYfM"
        # if not api_key:
        #     raise ValueError("API key is missing. Please set the environment variable.")

        # genai.configure(api_key=api_key)

        # # Create the model
        # generation_config = {
        #     "temperature": 1,
        #     "top_p": 0.95,
        #     "top_k": 64,
        #     "max_output_tokens": 8192,
        #     "response_mime_type": "text/plain",
        # }

        # model = genai.GenerativeModel(
        #     model_name="gemini-1.5-flash",
        #     generation_config=generation_config,
        # )

        # chat_session = model.start_chat(
        #     history=[]
        # )

        # try:
        #     message = "Make a feedback and advise for students to this result: " + json.dumps(result_dict)
        #     response_msg = chat_session.send_message(message)
        #     # response = chat_session.send_message("Make a feedback to this result, this is a students result", result_dict)
        #     print(response_msg.text)
        # except Exception as e:
        #     print(f"An error occurred: {e}")


        context = {
            'results': result,
            'info': infos,
            # 'ai_message': response_msg.text
        }
        return render(request, 'dashboard/students_result_show.html', context)
