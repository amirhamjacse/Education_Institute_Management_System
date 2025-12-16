from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, View
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin
)
import calendar
from django.contrib.auth.models import Group
from datetime import datetime
from students.models.students_info import StudentsInfo
from students.forms.studentscreateform import StudentsInfoForm
from students.forms.result_input import ResultInputForm
from Core.models import UserManager, User

# prfx = self.subscription
#             # print(prfx, prfx.subs_type, prfx.subs_type.prefixs, 'shdddd')
#             start_from = 1
#             i = generate_account_no(self.account_no, start_from, prfx.subs_type.prefixs) # noqa
#             while Accounts.objects.filter(account_no=i).exists():
#                 start_from += 1  # increment if id exists
#                 i = generate_account_no(self.account_no, start_from, prfx.subs_type.prefixs) # noqa
#             self.account_no = i

def generate_user_id(prefix):
    current_year = datetime.now().year  # get current year
    current_year = str(current_year)
    cu_first_two = current_year[:2]
    cu_last_two = datetime.now().strftime("%y")
    current_date = datetime.today()
    _, num_weeks = calendar.monthrange(current_date.year, current_date.month)
    week_number = (current_date.day - 1) // 7 + 1
    if current_date.day + 7 - (week_number - 1) * 7 > num_weeks * 7:
        week_number = num_weeks
    current_month = str(datetime.now().month)  # get current month
    if len(current_month) == 1:
        month = '0' + current_month
    else:
        current_month = current_month
    # count of data
    last_add = User.objects.values('user_id').last()
    # print(last_add, 'add-------')
    total_account = str(
        User.objects.values('user_id').count() + 1
    )
    # print(total_account, 'total-------------')
    if len(total_account) == 1:
        last_id = f'0000{total_account}'
    elif len(total_account) == 2:
        last_id = f'000{total_account}'
    elif len(total_account) == 3:
        last_id = f'00{total_account}'
    else:
        last_id = total_account
    # current_week_of_this_month
    user_id_no = f'{cu_last_two}{month}{week_number}{last_id}' # noqa
        # user_id_no = f'{prefix}{cu_last_two}00{cu_first_two}{month}{week_number}{last_id}' # noq
    return user_id_no


class StudentsCreateView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, CreateView
):

    model = StudentsInfo
    form_class = StudentsInfoForm
    permission_required = 'students.add_studentsinfo'
    template_name = 'studentsinfo/students_info_create.html'
    success_url = reverse_lazy('students:students_list')

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, *args, **kwargs):
        form_class = StudentsInfoForm
        group = Group.objects.all()
        context = {
            'form': form_class,
            'group': group
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = StudentsInfoForm(request.POST, request.FILES)
        user_manager = UserManager
        # print(form, 'form-----------------------')
        if form.is_valid():
            student_info_ins = form.save(commit=False)
            if student_info_ins.unique_roll:
                user = user_manager.create_user(
                    self=UserManager,
                    user_id=str(student_info_ins.unique_roll),
                    password=str(student_info_ins.personal_mobile_number),
                )
            else:
                user_id = generate_user_id(prefix=student_info_ins.section_class)
                # print(user_id, 'id------------------------')
                user = user_manager.create_user(
                    self=UserManager,
                    user_id=str(user_id),
                    password=str(student_info_ins.personal_mobile_number),
                )
                student_info_ins.unique_roll = user_id
            student_info_ins.save()
            print(user,)
            group = Group.objects.get(id=1)
            group.user_set.add(user)
            # user.groups.add(group)
            print(group, 'group')
        else:
            print(form.errors, 'Student Create Error')
        return redirect('students:students_list')



class StudentsListView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):

    model = StudentsInfo
    permission_required = 'students.view_studentsinfo'
    template_name = 'studentsinfo/students_list.html'

    def test_func(self):
        return self.request.user.is_active
    
    def get(self, request):
        stdn = self.model.objects.all().order_by('-id')
        # print(stdn, 'aa')
        # studentss = StudentsInfo.objects.get(id=1)
        # print(studentss)
        form = ResultInputForm()
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
