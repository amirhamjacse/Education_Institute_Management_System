"""institutemanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pipes import Template
from django.contrib import admin
from django.urls import path, include
from institute_dashaboard import views
from django.conf import settings
from django.conf.urls.static import static
from Core.views import IndexView, SignupView, LoginView
from django.views.generic import TemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('notice_board/', views.notice_board, name='notice_board'),
    # path('students_info/', views.students_info, name='students_info'),
    path('students_info/', views.StudentsInfoView.as_view(), name='students_info'),
    path('<int:id>/', views.students_details, name='students_details'),
    path('result/', views.result, name='result'),
    path('addmission/', views.OnlineAdmissionView.as_view(), name='onlineadm'),
    path('complain/', views.complain, name='complain'),
    path('contact/', views.contact_page, name='contact'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('teachers_info/', views.teachers_page, name='teachers_info'),
    path('other_employee/', views.stafs_page, name='staf'),
    path('cultural_program/', views.cultur, name='cultur'),
    path('sports/', views.sports, name='sports'),
    path('speach/', views.speach, name='speach'),
    path('lokko_uddessho/', views.lokkouddessho, name='lokko'),
    path('history/', views.clg_history, name='history'),
    path('news/', views.newspage, name='news'),
    path('news/', views.newspage, name='news'),
    path('student/', include('students.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('prms', include('django_prometheus.urls')),
    path('customize/', include('websitesetting.urls')),
    path('dashboard_management/', include('dashboard_management.urls')),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
