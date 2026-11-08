from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse

from students.models import StudentsInfo, Book
from institute_dashaboard.models import Teachers_Information, OnlineAdmission
from fees.models import Invoice


class AdminQuickSearchView(LoginRequiredMixin, View):
    """
    Spotlight live search API for students, teachers, invoices, books, and navigation.
    Triggered via global Ctrl+K / Cmd+K.
    """
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '').strip()
        if not q or len(q) < 2:
            return JsonResponse({'results': []})

        results = []

        # 1. System Navigation Commands / Shortcuts
        shortcuts = [
            {'title': 'Class Routine Matrix', 'subtitle': 'Academics timetable & scheduling', 'url': reverse('students:students_routine'), 'category': 'Tool', 'icon': 'bi-calendar3'},
            {'title': 'Admit Card Generator', 'subtitle': 'Print examination passes', 'url': reverse('students:admit_cards'), 'category': 'Tool', 'icon': 'bi-person-badge'},
            {'title': 'Online Admissions Manager', 'subtitle': 'Review & enroll applicants', 'url': reverse('dashboard_management:online_admission'), 'category': 'Tool', 'icon': 'bi-mortarboard'},
            {'title': 'Student ID Cards', 'subtitle': 'Generate and batch print ID cards', 'url': reverse('dashboard_management:student_id_cards'), 'category': 'Tool', 'icon': 'bi-person-vcard'},
            {'title': 'Library Book Catalog', 'subtitle': 'Manage books & circulation loans', 'url': reverse('students:library_catalog'), 'category': 'Tool', 'icon': 'bi-book'},
            {'title': 'Circulation Desk Issues', 'subtitle': 'Book loan issues & returns', 'url': reverse('students:library_issues'), 'category': 'Tool', 'icon': 'bi-journal-arrow-up'},
            {'title': 'Transport Fleet & Routes', 'subtitle': 'Vehicles, routes & passenger allocations', 'url': reverse('students:transport_list'), 'category': 'Tool', 'icon': 'bi-bus-front'},
            {'title': 'Hostel & Dormitory Roster', 'subtitle': 'Buildings, rooms & resident beds', 'url': reverse('students:hostel_list'), 'category': 'Tool', 'icon': 'bi-building'},
            {'title': 'Staff & Student Leaves', 'subtitle': 'Approve or reject leave applications', 'url': reverse('students:leave_manage'), 'category': 'Tool', 'icon': 'bi-calendar-check'},
            {'title': 'Teacher Daily Attendance', 'subtitle': 'Mark faculty attendance sheet', 'url': reverse('dashboard_management:teacher_attendance_mark'), 'category': 'Tool', 'icon': 'bi-check2-square'},
            {'title': 'Teacher Attendance Report', 'subtitle': 'Filter historical faculty attendance', 'url': reverse('dashboard_management:teacher_attendance_report'), 'category': 'Tool', 'icon': 'bi-bar-chart-line'},
            {'title': 'Assign Classes to Teachers', 'subtitle': 'Subject & class allocations', 'url': reverse('dashboard_management:assigned_class_teacher'), 'category': 'Tool', 'icon': 'bi-diagram-3'},
            {'title': 'Notice Board Announcements', 'subtitle': 'Publish campus notices & PDF circulars', 'url': reverse('dashboard_management:notice_adding'), 'category': 'Tool', 'icon': 'bi-bell'},
            {'title': 'News & Breaking Ticker', 'subtitle': 'Website news headlines', 'url': reverse('dashboard_management:news_adding'), 'category': 'Tool', 'icon': 'bi-newspaper'},
            {'title': 'Campus Photo Gallery', 'subtitle': 'Upload campus photographs', 'url': reverse('dashboard_management:gallery_list'), 'category': 'Tool', 'icon': 'bi-images'},
            {'title': 'Fee Invoices & Billing', 'subtitle': 'Fee structures and collection', 'url': reverse('fees:invoice_list'), 'category': 'Tool', 'icon': 'bi-receipt'},
            {'title': 'Public Parent Portal', 'subtitle': 'Guardian student overview', 'url': reverse('parents_portal'), 'category': 'Tool', 'icon': 'bi-people'},
        ]

        q_lower = q.lower()
        for s in shortcuts:
            if q_lower in s['title'].lower() or q_lower in s['subtitle'].lower():
                results.append(s)

        # 2. Students (Search by Name, Roll, Mobile)
        students = StudentsInfo.objects.filter(
            Q(name__icontains=q) |
            Q(unique_roll__icontains=q) |
            Q(personal_mobile_number__icontains=q)
        ).select_related('class_name', 'section_class')[:6]

        for s in students:
            cls_name = s.class_name.name if s.class_name else 'Unassigned'
            sec_name = f", Sec {s.section_class.name}" if s.section_class else ''
            results.append({
                'title': s.name,
                'subtitle': f"Class {cls_name}{sec_name} | Roll #{s.unique_roll or 'N/A'}",
                'url': reverse('students:students_details', kwargs={'id': s.id}) if hasattr(s, 'id') else reverse('students:students_list'),
                'category': 'Students',
                'icon': 'bi-person-circle'
            })

        # 3. Teachers & Faculty
        teachers = Teachers_Information.objects.filter(
            Q(teachers_name__icontains=q) |
            Q(designation__icontains=q) |
            Q(phone_number__icontains=q)
        )[:5]

        for t in teachers:
            results.append({
                'title': t.teachers_name,
                'subtitle': f"{t.designation or 'Faculty'} | {t.phone_number or ''}",
                'url': reverse('dashboard_management:assigned_class_teacher'),
                'category': 'Faculty',
                'icon': 'bi-person-badge-fill'
            })

        # 4. Invoices
        invoices = Invoice.objects.filter(
            Q(invoice_no__icontains=q) |
            Q(student__name__icontains=q)
        ).select_related('student')[:4]

        for inv in invoices:
            results.append({
                'title': f"Invoice {inv.invoice_no}",
                'subtitle': f"{inv.student.name if inv.student else 'Unknown'} | {inv.status} | ৳{inv.amount}",
                'url': reverse('fees:invoice_detail', kwargs={'pk': inv.pk}),
                'category': 'Finance',
                'icon': 'bi-receipt'
            })

        # 5. Library Books
        books = Book.objects.filter(
            Q(title__icontains=q) |
            Q(author__icontains=q) |
            Q(isbn__icontains=q)
        )[:4]

        for b in books:
            results.append({
                'title': b.title,
                'subtitle': f"By {b.author} | {b.available_copies}/{b.total_copies} available",
                'url': reverse('students:library_catalog'),
                'category': 'Library',
                'icon': 'bi-book-half'
            })

        return JsonResponse({'results': results})
