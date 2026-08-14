from django import forms
from django.core.exceptions import ValidationError

from fees.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'method', 'reference_no', 'paid_on', 'remarks']
        widgets = {
            'paid_on': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")
        return amount
