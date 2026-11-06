from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from .commonfields import CommonFields
from .students_info import StudentsInfo


class BookCategory(CommonFields):
    """Category classification for library books"""
    name = models.CharField(_('Category Name'), max_length=100, unique=True)
    code = models.CharField(_('Category Code'), max_length=50, blank=True, default='')
    description = models.TextField(_('Description'), blank=True, default='')

    def __str__(self):
        return self.name


class Book(CommonFields):
    """Library book catalog model"""
    category = models.ForeignKey(
        BookCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    title = models.CharField(_('Book Title'), max_length=255)
    author = models.CharField(_('Author(s)'), max_length=255)
    isbn = models.CharField(_('ISBN Number'), max_length=50, blank=True, default='')
    publisher = models.CharField(_('Publisher'), max_length=150, blank=True, default='')
    edition = models.CharField(_('Edition'), max_length=50, blank=True, default='')
    quantity = models.PositiveIntegerField(_('Total Copies'), default=1)
    available_copies = models.PositiveIntegerField(_('Available Copies'), default=1)
    rack_location = models.CharField(_('Rack / Shelf Location'), max_length=100, blank=True, default='Shelf A1')
    book_image = models.ImageField(_('Cover Image'), upload_to='books/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookIssue(CommonFields):
    """Book circulation tracking (issue and return)"""
    STATUS_CHOICES = [
        ('ISSUED', 'Issued'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
        ('LOST', 'Lost'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='issues'
    )
    student = models.ForeignKey(
        StudentsInfo,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='borrowed_books'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='issued_books'
    )
    issue_date = models.DateField(_('Issue Date'), default=timezone.now)
    due_date = models.DateField(_('Due Date'))
    return_date = models.DateField(_('Return Date'), null=True, blank=True)
    fine_amount = models.DecimalField(_('Fine Amount'), max_digits=8, decimal_places=2, default=0.00)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='ISSUED')
    remarks = models.TextField(_('Remarks'), blank=True, default='')
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books_issued_by'
    )

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        borrower = self.student.name if self.student else (self.user.get_full_name() or self.user.user_id)
        return f"{self.book.title} -> {borrower} ({self.status})"
