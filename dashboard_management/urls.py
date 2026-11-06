from django.urls import path
from dashboard_management import views

app_name = 'dashboard_management'

urlpatterns = [

    # online admission processing & enrollment
    path(
        'onlineadmission/',
        views.OnlineAdmissionProcess.as_view(),
        name='online_admission'
    ),
    path(
        'onlineadmission/enroll/<int:pk>/',
        views.OnlineAdmissionEnrollView.as_view(),
        name='online_admission_enroll'
    ),
    path(
        'onlineadmission/hold/<int:pk>/',
        views.OnlineAdmissionHoldToggleView.as_view(),
        name='online_admission_hold'
    ),
    path(
        'portelmanager/dashboard',
        views.PortalManagerDashboard.as_view(),
        name='portal_manager_board'
    ),
    path(
        'assigned/class',
        views.AssignClassesToTeacher.as_view(),
        name='assigned_class_teacher'
    ),
    path(
        'assigned/teacher/classes/',
        views.AssignClassesToTeacher.as_view(),
        name='assign_teacher_classes'
    ),
    path(
        'assigned/class/delete/<int:pk>/',
        views.DeleteTeacherAssignmentView.as_view(),
        name='delete_teacher_assignment'
    ),
    path(
        'portelmanager/id-cards',
        views.StudentIDCardView.as_view(),
        name='student_id_cards'
    ),
    path(
        'notice/adding',
        views.ADDNotice.as_view(),
        name='notice_adding'
    ),
    path('delete-notice/<int:notice_id>/',
         views.DeleteNotice.as_view(),
         name='delete_notice'),
    path(
        'news/adding',
        views.AddNews.as_view(),
        name='news_adding'
    ),
    path('delete-news/<int:news_id>/',
         views.DeleteNews.as_view(),
         name='delete_news'),

    path('galleries/', views.GalleryView.as_view(), name='gallery_list'),
    path('galleries/add/', views.GalleryView.as_view(), name='add_gallery'),
    path('galleries/edit/<int:gallery_id>/', views.GalleryView.as_view(), name='edit_gallery'),
    path('galleries/delete/<int:gallery_id>/', views.GalleryView.as_view(), name='delete_gallery'),
    
    path('add/teacher',
         views.AddTeacherView.as_view(),
         name='add_teacher'
        ),
    path('add/stuff',
         views.AddStuff.as_view(),
         name='add_stuff'
        ),

    path('attendance/teacher/',
         views.TeacherAttendanceMarkView.as_view(),
         name='teacher_attendance_mark'
        ),
    path('attendance/teacher/report/',
         views.TeacherAttendanceReportView.as_view(),
         name='teacher_attendance_report'
        ),

]