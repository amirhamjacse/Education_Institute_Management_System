from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db import transaction

from students.models import StudentsInfo, ClassName, SectionClas, Session
from institute_dashaboard.models import OnlineAdmission
from Core.models import User
from Core.utils import generate_temp_password


class OnlineAdmissionProcess(LoginRequiredMixin, UserPassesTestMixin, View):
    """List online admission applications with status filters and enrollment modal support"""
    template_name = 'online_admission.html'

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        status_filter = request.GET.get('status', 'active')
        qs = OnlineAdmission.objects.all().order_by('-id')

        if status_filter == 'active':
            qs = qs.filter(is_active=True, is_hold=False)
        elif status_filter == 'hold':
            qs = qs.filter(is_hold=True)
        elif status_filter == 'enrolled':
            qs = qs.filter(is_active=False, is_hold=False)

        classes = ClassName.objects.filter(is_active=True)
        sections = SectionClas.objects.filter(is_active=True)
        sessions = Session.objects.filter(is_active=True)

        context = {
            'online_admission_apply': qs,
            'classes': classes,
            'sections': sections,
            'sessions': sessions,
            'current_status': status_filter,
            'total_active': OnlineAdmission.objects.filter(is_active=True, is_hold=False).count(),
            'total_hold': OnlineAdmission.objects.filter(is_hold=True).count(),
            'total_enrolled': OnlineAdmission.objects.filter(is_active=False, is_hold=False).count(),
        }
        return render(request, self.template_name, context)


class OnlineAdmissionEnrollView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Enroll an applicant: create StudentsInfo + Core.User login credentials"""

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def post(self, request, pk, *args, **kwargs):
        application = get_object_or_404(OnlineAdmission, pk=pk)

        class_id = request.POST.get('class_name') or request.POST.get('class_id')
        section_id = request.POST.get('section_class') or request.POST.get('section_id')
        session_id = request.POST.get('session') or request.POST.get('session_id')
        unique_roll = (request.POST.get('unique_roll') or request.POST.get('roll_number', '')).strip()

        if not (class_id and section_id and session_id and unique_roll):
            messages.error(request, 'Class, Section, Session, and Roll Number are required.')
            return redirect('dashboard_management:online_admission')

        if StudentsInfo.objects.filter(unique_roll=unique_roll).exists():
            messages.error(request, f'Roll number {unique_roll} already exists. Please choose a different roll.')
            return redirect('dashboard_management:online_admission')

        try:
            with transaction.atomic():
                class_obj = ClassName.objects.get(pk=class_id)
                section_obj = SectionClas.objects.get(pk=section_id)
                
                session_name = str(session_id)
                if session_id and str(session_id).isdigit():
                    s_obj = Session.objects.filter(pk=session_id).first()
                    if s_obj:
                        session_name = s_obj.name

                # Create Core.User account
                raw_password = generate_temp_password(10)
                user = User.objects.create_user(
                    user_id=unique_roll,
                    password=raw_password,
                    first_name=application.student_name_en,
                    phone=application.student_number[:12] if application.student_number else None,
                )

                # Assign to Student group
                student_group, _ = Group.objects.get_or_create(name='Student')
                user.groups.add(student_group)

                # Create StudentsInfo
                student = StudentsInfo.objects.create(
                    name=application.student_name_en or application.student_name_bn,
                    unique_roll=unique_roll,
                    father_name=application.student_father_name_en or application.student_father_name_bn,
                    mother_name=application.student_mother_name_en or application.student_mother_name_bn,
                    date_of_birth=application.date_of_birth,
                    present_address=application.present_address,
                    permanent_address=application.permanent_address,
                    personal_mobile_number=application.student_number,
                    gurdian_mobile_number=application.gurdian_number,
                    admission_date=timezone.now().date(),
                    gender=application.gender_choise,
                    session=session_name[:12],
                    class_name=class_obj,
                    section_class=section_obj,
                    students_image=application.online_admission_pic,
                    user=user,
                )

                # Mark application as enrolled
                application.is_active = False
                application.is_hold = False
                application.save()

            messages.success(
                request,
                f"Successfully enrolled {student.name}! Assigned Roll: {unique_roll}. "
                f"Student Login ID: {user.user_id} | Temporary Password: {raw_password} (Please share this securely)."
            )
        except Exception as e:
            messages.error(request, f"Enrollment failed: {e}")

        return redirect('dashboard_management:online_admission')


class OnlineAdmissionHoldToggleView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Toggle hold status for an admission application"""

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def post(self, request, pk, *args, **kwargs):
        application = get_object_or_404(OnlineAdmission, pk=pk)
        application.is_hold = not application.is_hold
        application.save()
        status_text = "put on hold" if application.is_hold else "taken off hold"
        messages.info(request, f"Application for {application.student_name_en} {status_text}.")
        return redirect('dashboard_management:online_admission')
