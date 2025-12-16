from django import forms
from students.models.result import ResultInfo
from students.models.class_studn import ClassYear, ClassName


class ResultInputForm(forms.ModelForm):
    class Meta:
        model = ResultInfo
        fields = [
            # 'marks',
            # 'exam_type',
            # 'exam_year',

        ]

class AddResultstdlist(forms.ModelForm):
    class Meta:
        model = ResultInfo
        fields = [
            'exam_type',
            'exam_year',
            'class_name',
            'subject',
            'section',
        ]

class ClasYearForm(forms.ModelForm):
    class Meta:
        model = ClassName
        fields = [
            'class_nm',
        ]