# forms.py
from django import forms
from institute_dashaboard.models import Teachers_Information, Other_Employee_Information

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teachers_Information
        fields = ['teachers_name', 'phone_number', 'email', 'designation', 'teachers_photo']
        widgets = {
            'teachers_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'teachers_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class StuffForm(forms.ModelForm):
    class Meta:
        model = Other_Employee_Information
        fields = ['Others_name', 'phone_number', 'email', 'designation', 'Others_photo']
        widgets = {
            'Others_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'Others_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
