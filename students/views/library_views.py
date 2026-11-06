from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from students.models import BookCategory, Book, BookIssue, StudentsInfo
from Core.models import User
from institute_dashaboard.models import Web_Heading


class BookCatalogView(LoginRequiredMixin, View):
    """Browse and search library books"""
    template_name = 'library/book_list.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        cat_id = request.GET.get('category')

        books = Book.objects.filter(is_active=True).select_related('category')
        if q:
            books = books.filter(
                Q(title__icontains=q) | Q(author__icontains=q) |
                Q(isbn__icontains=q) | Q(publisher__icontains=q)
            )
        if cat_id:
            books = books.filter(category_id=cat_id)

        categories = BookCategory.objects.filter(is_active=True)
        webheading = Web_Heading.objects.last()

        context = {
            'books': books,
            'categories': categories,
            'search_query': q,
            'selected_cat': cat_id,
            'webname': webheading,
            'total_books': Book.objects.filter(is_active=True).count(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Add new book to library (staff only)"""
        if not request.user.is_staff:
            messages.error(request, 'Staff permissions required.')
            return redirect('students:library_catalog')

        title = request.POST.get('title')
        author = request.POST.get('author')
        category_id = request.POST.get('category')
        isbn = request.POST.get('isbn', '')
        publisher = request.POST.get('publisher', '')
        edition = request.POST.get('edition', '')
        quantity = int(request.POST.get('quantity', 1))
        rack_location = request.POST.get('rack_location', 'Shelf A1')

        try:
            cat_obj = BookCategory.objects.filter(id=category_id).first() if category_id else None
            Book.objects.create(
                title=title,
                author=author,
                category=cat_obj,
                isbn=isbn,
                publisher=publisher,
                edition=edition,
                quantity=quantity,
                available_copies=quantity,
                rack_location=rack_location,
            )
            messages.success(request, f'Book "{title}" added to library catalog successfully.')
        except Exception as e:
            messages.error(request, f'Failed to add book: {e}')

        return redirect('students:library_catalog')


class BookIssueManageView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Issue and return tracking for library (staff only)"""
    template_name = 'library/book_issues.html'

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        status_filter = request.GET.get('status', 'ISSUED')
        issues = BookIssue.objects.all().select_related('book', 'student', 'user', 'issued_by').order_by('-issue_date')

        if status_filter != 'ALL':
            issues = issues.filter(status=status_filter)

        books = Book.objects.filter(available_copies__gt=0, is_active=True)
        students = StudentsInfo.objects.filter(is_active=True)
        webheading = Web_Heading.objects.last()

        context = {
            'issues': issues,
            'books': books,
            'students_list': students,
            'current_status': status_filter,
            'webname': webheading,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Issue book to student"""
        book_id = request.POST.get('book')
        student_id = request.POST.get('student')
        days = int(request.POST.get('days', 14))

        book = get_object_or_404(Book, id=book_id)
        student = get_object_or_404(StudentsInfo, id=student_id)

        if book.available_copies <= 0:
            messages.error(request, 'No copies available for issue.')
            return redirect('students:library_issues')

        due_date = timezone.now().date() + timedelta(days=days)
        BookIssue.objects.create(
            book=book,
            student=student,
            user=student.user,
            due_date=due_date,
            status='ISSUED',
            issued_by=request.user
        )
        book.available_copies -= 1
        book.save()

        messages.success(request, f'Issued "{book.title}" to {student.name}. Due on {due_date}.')
        return redirect('students:library_issues')


class BookReturnActionView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Mark book as returned and assess fine if overdue"""
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def post(self, request, pk, *args, **kwargs):
        issue = get_object_or_404(BookIssue, pk=pk)
        today = timezone.now().date()
        issue.return_date = today

        # Fine calculation: 5 BDT per day overdue
        if today > issue.due_date:
            days_overdue = (today - issue.due_date).days
            fine = days_overdue * 5.0
            issue.fine_amount = fine
            issue.status = 'OVERDUE'
        else:
            issue.status = 'RETURNED'

        issue.save()

        # Restore available copies
        issue.book.available_copies += 1
        issue.book.save()

        messages.success(request, f'Book "{issue.book.title}" marked as returned. Fine assessed: {issue.fine_amount} BDT.')
        return redirect('students:library_issues')


class MyBooksView(LoginRequiredMixin, View):
    """Student/Teacher personal view of borrowed books and due dates"""
    template_name = 'library/my_books.html'

    def get(self, request, *args, **kwargs):
        my_issues = BookIssue.objects.none()
        if hasattr(request.user, 'student_profile'):
            my_issues = BookIssue.objects.filter(student=request.user.student_profile).select_related('book').order_by('-issue_date')
        elif request.user.is_authenticated:
            my_issues = BookIssue.objects.filter(user=request.user).select_related('book').order_by('-issue_date')

        webheading = Web_Heading.objects.last()
        return render(request, self.template_name, {
            'my_issues': my_issues,
            'webname': webheading,
        })
