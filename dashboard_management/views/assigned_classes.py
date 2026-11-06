from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from students.models import (
    TeacherAssignment, ClassName, SectionClas, Subjects, ClassYear
)
from institute_dashaboard.models import Teachers_Information, Web_Heading


class AssignClassesToTeacher(LoginRequiredMixin, View):
    """View and manage teacher class/subject assignments"""
    template_name = 'assigned_class.html'

    def get(self, request, *args, **kwargs):
        teachers = Teachers_Information.objects.all()
        classes = ClassName.objects.filter(is_active=True)
        sections = SectionClas.objects.filter(is_active=True)
        subjects = Subjects.objects.filter(is_active=True)
        years = ClassYear.objects.filter(is_active=True)

        selected_teacher_id = request.GET.get('teacher')

        # Auto-detect if logged-in user is a teacher
        if hasattr(request.user, 'teacher_profile') and not selected_teacher_id:
            selected_teacher_id = str(request.user.teacher_profile.id)

        assignments = TeacherAssignment.objects.all().select_related(
            'teacher', 'class_name', 'section', 'subject', 'academic_year'
        )
        if selected_teacher_id:
            assignments = assignments.filter(teacher_id=selected_teacher_id)

        webheading = Web_Heading.objects.last()

        context = {
            'teachers': teachers,
            'classes': classes,
            'sections': sections,
            'subjects': subjects,
            'years': years,
            'assignments': assignments,
            'selected_teacher_id': selected_teacher_id,
            'webname': webheading,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Create new teacher assignment (staff/admin only)"""
        if not request.user.is_staff:
            messages.error(request, 'Staff permissions required.')
            return redirect('dashboard_management:assigned_class_teacher')

        teacher_id = request.POST.get('teacher')
        class_id = request.POST.get('class_name')
        section_id = request.POST.get('section')
        subject_id = request.POST.get('subject')
        year_id = request.POST.get('academic_year')

        if not (teacher_id and class_id and section_id and subject_id):
            messages.error(request, 'Teacher, Class, Section, and Subject are all required.')
            return redirect('dashboard_management:assigned_class_teacher')

        teacher = get_object_or_404(Teachers_Information, id=teacher_id)
        class_obj = get_object_or_404(ClassName, id=class_id)
        section = get_object_or_404(SectionClas, id=section_id)
        subject = get_object_or_404(Subjects, id=subject_id)
        year = ClassYear.objects.filter(id=year_id).first() if year_id else None

        assignment, created = TeacherAssignment.objects.update_or_create(
            teacher=teacher,
            class_name=class_obj,
            section=section,
            subject=subject,
            defaults={'academic_year': year, 'is_active': True}
        )
        if created:
            messages.success(request, f'Assigned {subject.name} in {class_obj.name} ({section.name}) to {teacher.teachers_name}.')
        else:
            messages.info(request, f'Updated assignment for {teacher.teachers_name}.')

        return redirect(f"{request.path}?teacher={teacher_id}")


class DeleteTeacherAssignmentView(LoginRequiredMixin, View):
    """Remove a teacher assignment"""
    def post(self, request, pk, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Staff permissions required.')
            return redirect('dashboard_management:assigned_class_teacher')

        assignment = get_object_or_404(TeacherAssignment, pk=pk)
        teacher_id = assignment.teacher_id
        assignment.delete()
        messages.success(request, 'Assignment removed.')
        return redirect(f"/dashboard_management/assigned/class?teacher={teacher_id}")
