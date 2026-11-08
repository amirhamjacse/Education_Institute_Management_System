from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction

from students.models import (
    ClassName, SectionClas, Subjects, TimeSlot,
    ClassRoutine, TeacherAssignment, Exam, ExamYear,
    ExamAdmitCard, StudentsInfo
)
from institute_dashaboard.models import Teachers_Information, Web_Heading


class RoutineView(LoginRequiredMixin, View):
    """Dynamic visual timetable for students, teachers, and staff"""
    template_name = 'dashboard/students_routine.html'

    def get(self, request, *args, **kwargs):
        classes = ClassName.objects.filter(is_active=True)
        sections = SectionClas.objects.filter(is_active=True)
        time_slots = TimeSlot.objects.filter(is_active=True).order_by('start_time')
        teachers = Teachers_Information.objects.all()
        subjects = Subjects.objects.filter(is_active=True)

        selected_class_id = request.GET.get('class_name') or request.GET.get('class_id')
        selected_section_id = request.GET.get('section') or request.GET.get('section_id')

        # Auto-detect class/section for logged-in student
        if not selected_class_id and hasattr(request.user, 'student_profile'):
            student = request.user.student_profile
            selected_class_id = str(student.class_name_id) if student.class_name else None
            selected_section_id = str(student.section_class_id) if student.section_class else None

        # Fallback to first class/section
        if not selected_class_id and classes.exists():
            selected_class_id = str(classes.first().id)
        if not selected_section_id and sections.filter(class_nm_id=selected_class_id).exists():
            selected_section_id = str(sections.filter(class_nm_id=selected_class_id).first().id)

        selected_class = None
        selected_section = None
        if selected_class_id:
            selected_class = ClassName.objects.filter(id=selected_class_id).first()
        if selected_section_id:
            selected_section = SectionClas.objects.filter(id=selected_section_id).first()

        days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

        # Build timetable matrix: matrix[day][time_slot_id] = routine_entry
        routine_matrix = {day: {} for day in days}
        if selected_class and selected_section:
            routines = ClassRoutine.objects.filter(
                class_name=selected_class,
                section=selected_section,
                is_active=True
            ).select_related('subject', 'teacher', 'time_slot')

            for r in routines:
                if r.day_of_week in routine_matrix:
                    routine_matrix[r.day_of_week][r.time_slot_id] = r

        # Build structured routine_grid with smart conflict detection
        routine_grid = []
        for day in days:
            slots_data = []
            for slot in time_slots:
                entry = routine_matrix[day].get(slot.id)
                conflict_warning = None
                if entry and entry.teacher:
                    clash = ClassRoutine.objects.filter(
                        day_of_week=day,
                        time_slot=slot,
                        teacher=entry.teacher,
                        is_active=True
                    ).exclude(class_name=selected_class, section=selected_section).select_related('class_name', 'section').first()
                    if clash:
                        conflict_warning = f"Faculty double-booked: Also scheduled in Class {clash.class_name.name} ({clash.section.name})"

                slots_data.append({
                    'slot': slot,
                    'entry': entry,
                    'conflict': conflict_warning
                })
            routine_grid.append({
                'day': day,
                'slots': slots_data
            })

        webheading = Web_Heading.objects.last()

        context = {
            'classes': classes,
            'sections': sections,
            'time_slots': time_slots,
            'teachers': teachers,
            'subjects': subjects,
            'selected_class': selected_class,
            'selected_section': selected_section,
            'days': days,
            'routine_matrix': routine_matrix,
            'routine_grid': routine_grid,
            'webname': webheading,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Add or update routine slot entry (staff/admin only)"""
        if not request.user.is_staff:
            messages.error(request, 'Permission denied.')
            return redirect('students:students_routine')

        class_id = request.POST.get('class_name') or request.POST.get('class_id')
        section_id = request.POST.get('section') or request.POST.get('section_id')
        subject_id = request.POST.get('subject') or request.POST.get('subject_id')
        teacher_id = request.POST.get('teacher') or request.POST.get('teacher_id')
        time_slot_id = request.POST.get('time_slot') or request.POST.get('time_slot_id')
        day_of_week = request.POST.get('day_of_week') or request.POST.get('day')
        room_number = request.POST.get('room_number', 'Room 101')

        try:
            class_obj = ClassName.objects.get(id=class_id)
            section_obj = SectionClas.objects.get(id=section_id)
            subject_obj = Subjects.objects.get(id=subject_id)
            time_slot_obj = TimeSlot.objects.get(id=time_slot_id)
            teacher_obj = Teachers_Information.objects.filter(id=teacher_id).first() if teacher_id else None

            ClassRoutine.objects.update_or_create(
                class_name=class_obj,
                section=section_obj,
                time_slot=time_slot_obj,
                day_of_week=day_of_week,
                defaults={
                    'subject': subject_obj,
                    'teacher': teacher_obj,
                    'room_number': room_number,
                    'is_active': True,
                }
            )
            messages.success(request, f'Routine slot for {day_of_week} ({time_slot_obj.period_name}) saved successfully.')
        except Exception as e:
            messages.error(request, f'Failed to save routine: {e}')

        return redirect(f"{request.path}?class_name={class_id}&section={section_id}")


class DeleteRoutineSlotView(LoginRequiredMixin, View):
    """Delete a routine slot"""
    def post(self, request, pk, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Permission denied.')
            return redirect('students:students_routine')

        routine = get_object_or_404(ClassRoutine, pk=pk)
        class_id = routine.class_name_id
        sec_id = routine.section_id
        routine.delete()
        messages.success(request, 'Routine slot removed successfully.')
        return redirect(f"/student/routine/?class_name={class_id}&section={sec_id}")


class AdmitCardListView(LoginRequiredMixin, View):
    """Manage and generate exam admit cards"""
    template_name = 'dashboard/admit_card_list.html'

    def get(self, request, *args, **kwargs):
        classes = ClassName.objects.filter(is_active=True)
        sections = SectionClas.objects.filter(is_active=True)
        exams = Exam.objects.filter(is_active=True)
        exam_years = ExamYear.objects.filter(is_active=True)

        selected_exam_id = request.GET.get('exam')
        selected_year_id = request.GET.get('exam_year')
        selected_class_id = request.GET.get('class_name')
        selected_sec_id = request.GET.get('section')

        admit_cards = ExamAdmitCard.objects.all().select_related('student', 'exam', 'exam_year')

        # Auto-scope for student
        if hasattr(request.user, 'student_profile'):
            admit_cards = admit_cards.filter(student=request.user.student_profile)
        else:
            if selected_exam_id:
                admit_cards = admit_cards.filter(exam_id=selected_exam_id)
            if selected_year_id:
                admit_cards = admit_cards.filter(exam_year_id=selected_year_id)
            if selected_class_id:
                admit_cards = admit_cards.filter(student__class_name_id=selected_class_id)
            if selected_sec_id:
                admit_cards = admit_cards.filter(student__section_class_id=selected_sec_id)

        context = {
            'classes': classes,
            'sections': sections,
            'exams': exams,
            'exam_years': exam_years,
            'admit_cards': admit_cards,
            'selected_exam_id': selected_exam_id,
            'selected_year_id': selected_year_id,
            'selected_class_id': selected_class_id,
            'selected_sec_id': selected_sec_id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Bulk generate admit cards for a class & section"""
        if not request.user.is_staff:
            messages.error(request, 'Staff permissions required.')
            return redirect('students:admit_cards')

        exam_id = request.POST.get('exam')
        exam_year_id = request.POST.get('exam_year')
        class_id = request.POST.get('class_name')
        section_id = request.POST.get('section')
        room_prefix = request.POST.get('room_prefix', 'Hall A')

        if not (exam_id and exam_year_id and class_id):
            messages.error(request, 'Exam, Exam Year, and Class are required.')
            return redirect('students:admit_cards')

        exam = get_object_or_404(Exam, id=exam_id)
        exam_year = get_object_or_404(ExamYear, id=exam_year_id)
        students = StudentsInfo.objects.filter(class_name_id=class_id, is_active=True)
        if section_id:
            students = students.filter(section_class_id=section_id)

        created_count = 0
        for idx, student in enumerate(students, start=1):
            roll_str = student.unique_roll or str(student.id)
            bench_str = f"Seat #{idx:02d}"
            _, created = ExamAdmitCard.objects.update_or_create(
                student=student,
                exam=exam,
                exam_year=exam_year,
                defaults={
                    'roll_number': roll_str,
                    'room_number': room_prefix,
                    'seat_bench': bench_str,
                    'is_approved': True,
                }
            )
            if created:
                created_count += 1

        messages.success(request, f'Generated {created_count} admit cards for {exam.name}.')
        return redirect(f"{request.path}?exam={exam_id}&exam_year={exam_year_id}&class_name={class_id}")


class AdmitCardPrintView(LoginRequiredMixin, View):
    """Printable single or batch admit card with photo and exam instructions"""
    template_name = 'dashboard/admit_card_print.html'

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            admit_cards = ExamAdmitCard.objects.filter(pk=pk)
        else:
            exam_id = request.GET.get('exam')
            class_id = request.GET.get('class_name')
            section_id = request.GET.get('section')
            admit_cards = ExamAdmitCard.objects.filter(is_approved=True)
            if exam_id:
                admit_cards = admit_cards.filter(exam_id=exam_id)
            if class_id:
                admit_cards = admit_cards.filter(student__class_name_id=class_id)
            if section_id:
                admit_cards = admit_cards.filter(student__section_class_id=section_id)

        # Security check for student role
        if hasattr(request.user, 'student_profile'):
            admit_cards = admit_cards.filter(student=request.user.student_profile)

        webheading = Web_Heading.objects.last()
        return render(request, self.template_name, {
            'admit_cards': admit_cards,
            'webname': webheading,
        })
