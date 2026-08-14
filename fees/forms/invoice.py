from django import forms

from fees.models import FeeStructure, Invoice
from students.models.class_studn import ClassName, SectionClas
from students.models.students_info import StudentsInfo


class InvoiceGenerateQueryForm(forms.Form):
    class_name = forms.ModelChoiceField(
        queryset=ClassName.objects.filter(is_active=True),
        label="Class"
    )
    section = forms.ModelChoiceField(
        queryset=SectionClas.objects.filter(is_active=True),
        required=False, label="Section (optional — all sections if blank)"
    )
    fee_structure = forms.ModelChoiceField(
        queryset=FeeStructure.objects.filter(is_active=True).select_related(
            'fee_head', 'class_name'
        ),
        label="Fee Structure"
    )
    period_label = forms.CharField(
        max_length=30, required=False,
        help_text='e.g. "January 2026", "Term 1"',
        label="Period"
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Due Date"
    )


class AdHocInvoiceForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=StudentsInfo.objects.filter(is_deleted=False).order_by('name')
    )

    class Meta:
        model = Invoice
        fields = [
            'student', 'fee_head', 'amount', 'discount',
            'due_date', 'period_label', 'remarks',
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
