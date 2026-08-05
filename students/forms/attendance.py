from django import forms
from students.models.class_studn import ClassName, SectionClas


class AttendanceQueryForm(forms.Form):
    class_name = forms.ModelChoiceField(
        queryset=ClassName.objects.filter(is_active=True),
        label="Class"
    )
    section = forms.ModelChoiceField(
        queryset=SectionClas.objects.filter(is_active=True),
        label="Section"
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date"
    )
