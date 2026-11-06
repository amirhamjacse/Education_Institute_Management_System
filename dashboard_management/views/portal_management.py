from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, TemplateView, View
)
from students.models import StudentsInfo
from institute_dashaboard.models import (
    OnlineAdmission, complain, Notice_board, News_headline, Gallery
)
from dashboard_management.forms import (
    NoticeBoardForm, NewsdForm, GalleryForm, TeacherForm,
    StuffForm
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Group

from Core.models import User
from Core.utils import generate_temp_password, generate_prefixed_user_id


class PortalManagerDashboard(
    LoginRequiredMixin, UserPassesTestMixin, 
    TemplateView
):
    template_name = 'portal_manager_dashboard.html'

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from students.models import (
            StudentsInfo, ClassName, SectionClas,
            Book, BookIssue, Vehicle, TransportRoute,
            Hostel, HostelRoom, BedAllocation,
            LeaveApplication, ExamAdmitCard
        )
        from institute_dashaboard.models import (
            Notice_board, News_headline, Gallery,
            Teachers_Information, Other_Employee_Information,
            OnlineAdmission, Web_Heading
        )
        from fees.models import Invoice

        # Class-wise distribution
        classes_with_counts = []
        for c in ClassName.objects.all()[:6]:
            classes_with_counts.append({
                'class': c,
                'count': StudentsInfo.objects.filter(class_name=c).count()
            })

        context.update({
            'webname': Web_Heading.objects.last(),
            'total_students': StudentsInfo.objects.count(),
            'total_teachers': Teachers_Information.objects.count(),
            'total_staff': Other_Employee_Information.objects.count(),
            'total_classes': ClassName.objects.count(),
            'total_sections': SectionClas.objects.count(),
            
            # Admissions & Applications
            'total_online_pending': OnlineAdmission.objects.filter(is_active=True).count(),
            'recent_applicants': OnlineAdmission.objects.order_by('-id')[:5],

            # Library & Operations
            'total_books': Book.objects.count(),
            'books_issued': BookIssue.objects.filter(status='ISSUED').count(),
            'total_vehicles': Vehicle.objects.count(),
            'total_routes': TransportRoute.objects.count(),
            'total_hostels': Hostel.objects.count(),
            'total_beds_occupied': BedAllocation.objects.count(),

            # HR & Leaves
            'pending_leaves_count': LeaveApplication.objects.filter(status='PENDING').count(),
            'recent_leaves': LeaveApplication.objects.filter(status='PENDING').select_related('applicant', 'leave_type')[:5],

            # Invoices & Fees
            'total_invoices_count': Invoice.objects.count(),
            'recent_invoices': Invoice.objects.order_by('-id')[:5],

            # Content & Notif
            'total_notices': Notice_board.objects.count(),
            'total_news': News_headline.objects.count(),
            'total_gallery': Gallery.objects.count(),
            'recent_notices': Notice_board.objects.order_by('-id')[:5],
            'recent_news': News_headline.objects.order_by('-id')[:5],
            'classes_distribution': classes_with_counts,
        })
        return context



class ADDNotice(
    LoginRequiredMixin, UserPassesTestMixin,
    # PermissionRequiredMixin,
      View
):
    template_name = 'add_notice.html'
    # permission_required = 'dashboard_management.view_dashboard_management'

    def test_func(self):
        return self.request.user.is_active
    
    def get(self, request):
        notice = Notice_board.objects.all()
        form = NoticeBoardForm()
        context = {
            'notice': notice,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = NoticeBoardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice uploaded successfully!')
            return redirect('dashboard_management:notice_adding')  # Adjust the URL to your routing
        notice = Notice_board.objects.all()
        context = {
            'notice': notice,
            'form': form
        }
        return render(request, self.template_name, context)


class DeleteNotice(View):
    def post(self, request, notice_id):
        notice = get_object_or_404(Notice_board, id=notice_id)
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('dashboard_management:notice_adding')  # Adjust the URL to your routing
    

class AddNews(
    LoginRequiredMixin, UserPassesTestMixin,
    # PermissionRequiredMixin,
      View
):
    template_name = 'add_news.html'
    # permission_required = 'dashboard_management.view_dashboard_management'

    def test_func(self):
        return self.request.user.is_active
    
    def get(self, request):
        notice = News_headline.objects.all()
        form = NewsdForm()
        context = {
            'notice': notice,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = NewsdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'News headline published successfully!')
            return redirect('dashboard_management:news_adding')
        notice = News_headline.objects.all()
        context = {
            'notice': notice,
            'form': form
        }
        return render(request, self.template_name, context)


class DeleteNews(View):
    def post(self, request, news_id):
        notice = get_object_or_404(News_headline, id=news_id)
        notice.delete()
        messages.success(request, 'News deleted successfully!')
        return redirect('dashboard_management:news_adding')  # Adjust the URL to your routing


class GalleryView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'gallery_management.html'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request, gallery_id=None):
        if gallery_id:
            gallery = get_object_or_404(Gallery, id=gallery_id)
            form = GalleryForm(instance=gallery)
            action = 'edit'
        else:
            gallery = None
            form = GalleryForm()
            action = 'add'

        galleries = Gallery.objects.all()
        return render(request, self.template_name, {
            'form': form,
            'galleries': galleries,
            'action': action,
            'gallery': gallery,
        })

    def post(self, request, gallery_id=None):
        if 'delete' in request.path or request.POST.get('action') == 'delete':
            return self.delete(request, gallery_id)

        if gallery_id:
            gallery = get_object_or_404(Gallery, id=gallery_id)
            form = GalleryForm(request.POST, request.FILES, instance=gallery)
        else:
            form = GalleryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            if gallery_id:
                messages.success(request, 'Photo updated successfully!')
            else:
                messages.success(request, 'Photo added successfully!')
            return redirect('dashboard_management:gallery_list')

        galleries = Gallery.objects.all()
        return render(request, self.template_name, {
            'form': form,
            'galleries': galleries,
            'action': 'edit' if gallery_id else 'add',
            'gallery': gallery if gallery_id else None,
        })

    def delete(self, request, gallery_id):
        gallery = get_object_or_404(Gallery, id=gallery_id)
        gallery.delete()
        messages.success(request, 'Photo deleted successfully!')
        return redirect('dashboard_management:gallery_list')


class AddTeacherView(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'add_teacher.html'
    permission_required = 'institute_dashaboard.add_teachers_information'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        form = TeacherForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)

            user_id = generate_prefixed_user_id('TCH')
            temp_password = generate_temp_password()
            user = User.objects.create_user(
                user_id=user_id, password=temp_password,
                phone=teacher.phone_number,
            )
            teacher.user = user
            teacher.save()

            group, _ = Group.objects.get_or_create(name='Teacher')
            user.groups.add(group)

            messages.success(
                request,
                f'Teacher added. Login ID: {user_id}  '
                f'Temporary password: {temp_password} — '
                f'share this securely with the teacher.'
            )
            return redirect('teachers_info')  # Adjust the URL name as needed
        return render(request, self.template_name, {'form': form})


class AddStuff(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, View
):
    template_name = 'add_stuff.html'
    permission_required = 'institute_dashaboard.add_other_employee_information'

    def test_func(self):
        return self.request.user.is_active

    def get(self, request):
        form = StuffForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StuffForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save(commit=False)

            user_id = generate_prefixed_user_id('STF')
            temp_password = generate_temp_password()
            user = User.objects.create_user(
                user_id=user_id, password=temp_password,
                phone=staff.phone_number,
            )
            staff.user = user
            staff.save()

            group, _ = Group.objects.get_or_create(name='Staff')
            user.groups.add(group)

            messages.success(
                request,
                f'Stuff added. Login ID: {user_id}  '
                f'Temporary password: {temp_password} — '
                f'share this securely with the staff member.'
            )
            return redirect('staf')  # Adjust the URL name as needed
        return render(request, self.template_name, {'form': form})


