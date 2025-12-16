from django import forms
from students.models.students_info import StudentsInfo

class StudentsInfoForm(forms.ModelForm):
    class Meta:
        model = StudentsInfo
        fields = (
            'name',
            'unique_roll',
            'father_name',
            'mother_name',
            'students_image',
            'date_of_birth',
            'present_address',
            'permanent_address',
            'personal_mobile_number',
            'gurdian_mobile_number',
            'admission_date',
            'gender',
            'class_name',
            'section_class',
        )