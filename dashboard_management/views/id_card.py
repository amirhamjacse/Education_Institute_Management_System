from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from students.models import StudentsInfo, ClassName, SectionClas


class StudentIDCardView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'student_id_cards.html'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        classes = ClassName.objects.all().order_by('name')

        selected_class_id = request.GET.get('class_name', '')
        selected_section_id = request.GET.get('section', '')

        sections = SectionClas.objects.none()
        id_card_students = StudentsInfo.objects.none()

        if selected_class_id:
            sections = SectionClas.objects.filter(class_nm_id=selected_class_id).order_by('name')

            id_card_students = StudentsInfo.objects.filter(
                class_name_id=selected_class_id
            ).select_related('class_name', 'section_class')

            if selected_section_id:
                id_card_students = id_card_students.filter(section_class_id=selected_section_id)

            id_card_students = id_card_students.order_by('unique_roll', 'name')

        context = {
            'classes': classes,
            'sections': sections,
            'id_card_students': id_card_students,
            'selected_class_id': selected_class_id,
            'selected_section_id': selected_section_id,
        }
        return render(request, self.template_name, context)
