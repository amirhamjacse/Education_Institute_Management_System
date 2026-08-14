from django import forms

from fees.models import FeeHead, FeeStructure
from students.models.class_studn import ClassName


class FeeHeadForm(forms.ModelForm):
    class Meta:
        model = FeeHead
        fields = ['name', 'code', 'description']


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['fee_head', 'class_name', 'session', 'frequency', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fee_head'].queryset = FeeHead.objects.filter(is_active=True)
        self.fields['class_name'].queryset = ClassName.objects.filter(is_active=True)
