from django import forms
from .models import OnlineAdmission, complain

class OnlineAdmissionForm(forms.ModelForm):
    class Meta:
        model = OnlineAdmission
        fields = ['student_name_bn', 'student_name_en', 'student_father_name_bn', 'student_father_name_en', 'student_mother_name_bn', 'student_mother_name_en', 'gender_choise', 'student_number', 'gurdian_number', 'date_of_birth', 'present_address', 'permanent_address','online_admission_pic', 'admission_fee']
        labels = {'student_name_bn': 'আবেদনকারীর নাম (বাংলায়)', 'student_name_en' : 'আবেদনকারীর নাম (ইংরেজী)', 'student_father_name_bn' : 'পিতার নাম (বাংলায়)', 'student_father_name_en' : 'পিতার নাম (ইংরেজী)', 'student_mother_name_bn' : 'মাতার নাম (বাংলায়)', 'student_mother_name_en': 'মাতার নাম (ইংরেজী)', 'gender_choise' : 'লিঙ্গ', 'student_number' : 'আবেদনকারীর নাম্বার', 'gurdian_number' : 'অবিভাবকের নাম্বার', 'date_of_birth' : 'জন্ম তারিখ', 'present_address' : 'বর্তমান ঠিকানা', 'permanent_address' : 'স্থায়ী ঠিকানা','online_admission_pic' : 'আবেদনকারীর ছবি'}
        widgets = {
            'student_name_bn': forms.TextInput(attrs={'class': 'form-control'}),
            'student_name_en' : forms.TextInput(attrs={'class': 'form-control'}),
            'student_father_name_bn' : forms.TextInput(attrs={'class': 'form-control'}),
            'student_father_name_en' : forms.TextInput(attrs={'class': 'form-control'}),
            'student_mother_name_bn' : forms.TextInput(attrs={'class': 'form-control'}),
            'student_mother_name_en': forms.TextInput(attrs={'class': 'form-control'}),
            'gender_choise' : forms.Select(attrs={'class': 'form-select'}),
            'student_number' : forms.NumberInput(attrs={'class': 'form-control'}),
            'admission_fee' : forms.NumberInput(attrs={'class': 'form-control'}),
            'gurdian_number' : forms.NumberInput(attrs={'class': 'form-control'}),
            'date_of_birth' : forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'present_address' : forms.Textarea(attrs={'class': 'form-control', 'aria-label':'Sizing example input', 'cols': '1', 'rows': '3'}), 
            'permanent_address' : forms.Textarea(attrs={'class': 'form-control', 'aria-label':'Sizing example input', 'cols': '1', 'rows': '3'}),
            'online_admission_pic' : forms.FileInput(attrs={'class': 'form-control'}),
            
        }

class complainform(forms.ModelForm):
    class Meta:
        model = complain
        fields = ['name', 'email', 'mobile', 'address', 'complain_box']
        labels = {'name': 'আপনার নাম*', 'email': 'ইমেইল (অপশনাল) ', 'mobile': 'মোবাইল*', 'address': 'ঠিকানা (অপশনাল)', 'complain_box':'অভিযোগ বা পরামর্শ লিখুন এখানে*'}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}), 'email':forms.EmailInput(attrs={'class': 'form-control'}), 'mobile':forms.TextInput(attrs={'class': 'form-control'}), 'address':forms.Textarea(attrs={'class': 'form-control', 'aria-label':'Sizing example input', 'cols': '1', 'rows': '3'}), 'complain_box':forms.Textarea(attrs={'class': 'form-control', 'aria-label':'Sizing example input', 'cols': '1', 'rows': '3'})}
