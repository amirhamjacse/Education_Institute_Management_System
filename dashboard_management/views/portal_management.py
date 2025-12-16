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


class PortalManagerDashboard(
    LoginRequiredMixin, UserPassesTestMixin,
    PermissionRequiredMixin, 
    TemplateView
):
    template_name = 'portal_manager_dashboard.html'
    permission_required = 'dashboard_management.view_dashboard_management'

    def test_func(self):
        return self.request.user.is_active



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
            messages.success(request, 'Notice uploaded successfully!')
            return redirect('dashboard_management:notice_adding')  # Adjust the URL to your routing
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


class GalleryView(View):
    template_name = 'gallery_management.html'

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
            return redirect('dashboard_management:gallery_list')  # Adjust the URL as needed

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
        return redirect('gallery_list')  # Adjust the URL as needed


class AddTeacherView(View):
    template_name = 'add_teacher.html'

    def get(self, request):
        form = TeacherForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully!')
            return redirect('teachers_info')  # Adjust the URL name as needed
        return render(request, self.template_name, {'form': form})


class AddStuff(View):
    template_name = 'add_stuff.html'

    def get(self, request):
        form = StuffForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = StuffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stuff added successfully!')
            return redirect('staf')  # Adjust the URL name as needed
        return render(request, self.template_name, {'form': form})


