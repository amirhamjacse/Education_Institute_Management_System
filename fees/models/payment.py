from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from students.models.commonfields import CommonFields
from .invoice import Invoice

PAYMENT_METHOD = (
    ('cash', 'Cash'),
    ('bank', 'Bank Transfer'),
    ('mobile_banking', 'Mobile Banking'),
    ('other', 'Other'),
)


class Payment(CommonFields):
    receipt_no = models.CharField(
        _("Receipt No"), max_length=30, unique=True,
        editable=False, blank=True
    )
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE,
        verbose_name="Invoice", related_name='payments'
    )
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    method = models.CharField(
        _("Method"), max_length=15, choices=PAYMENT_METHOD, default='cash'
    )
    reference_no = models.CharField(
        _("Reference No"), max_length=100, blank=True, null=True
    )
    paid_on = models.DateField(_("Paid On"), default=timezone.now)
    remarks = models.CharField(
        _("Remarks"), max_length=255, blank=True, null=True
    )
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name="Received By",
        related_name='payments_received'
    )

    class Meta:
        ordering = ['-paid_on', '-created_time']

    def __str__(self):
        return f"{self.receipt_no} - {self.invoice.invoice_no}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.receipt_no:
            self.receipt_no = f"RCP-{self.pk:06d}"
            super().save(update_fields=['receipt_no'])
