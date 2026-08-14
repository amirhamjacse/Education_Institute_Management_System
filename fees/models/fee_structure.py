from django.db import models
from django.utils.translation import gettext_lazy as _

from students.models.commonfields import CommonFields
from students.models.class_studn import ClassName
from .fee_head import FeeHead

FREQUENCY_CHOICES = (
    ('one_time', 'One Time'),
    ('monthly', 'Monthly'),
    ('term', 'Term/Quarterly'),
    ('yearly', 'Yearly'),
)


class FeeStructure(CommonFields):
    fee_head = models.ForeignKey(
        FeeHead, on_delete=models.PROTECT,
        verbose_name="Fee Head", related_name='structures'
    )
    class_name = models.ForeignKey(
        ClassName, on_delete=models.CASCADE,
        verbose_name="Class", related_name='fee_structures'
    )
    # Free-text, not an FK: StudentsInfo.session is also a free-text
    # CharField, so bulk invoice generation can match students by an
    # exact string comparison against this field.
    session = models.CharField(_("Session"), max_length=20)
    frequency = models.CharField(
        _("Frequency"), max_length=10,
        choices=FREQUENCY_CHOICES, default='monthly'
    )
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('fee_head', 'class_name', 'session', 'frequency')
        ordering = ['class_name', 'fee_head']

    def __str__(self):
        return f"{self.class_name} - {self.fee_head} ({self.session})"
