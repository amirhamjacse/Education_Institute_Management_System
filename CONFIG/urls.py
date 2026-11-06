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
from django.contrib import admin
from django.urls import path, include
from institute_dashaboard import views
from django.conf import settings
from django.conf.urls.static import static
from Core.views import IndexView, SignupView, LoginView
from django.views.generic import TemplateView
from students.views.parent_views import ParentPortalView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('notice_board/', views.notice_board, name='notice_board'),
    path('students_info/', views.StudentsInfoView.as_view(), name='students_info'),
    path('student-details/<int:id>/', views.students_details, name='students_details'),
    path('<int:id>/', views.students_details, name='students_details_legacy'),
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
    path('parents/', ParentPortalView.as_view(), name='parents_portal'),
    path('student/', include('students.urls')),
    path('fees/', include('fees.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('core/', include('Core.urls', namespace='core')),
    path('prms', include('django_prometheus.urls')),
    path('customize/', include('websitesetting.urls')),
    path('dashboard_management/', include('dashboard_management.urls')),
    # SSLCommerz Payment Callbacks
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/faild/', views.payment_failed, name='payment_failed'),
    path('payment/cancel/', views.payment_canceled, name='payment_canceled'),
    path('payment/ipn/', views.payment_ipn, name='payment_ipn'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
