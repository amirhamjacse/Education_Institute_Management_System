from django.urls import path
from dashboard_management import views

app_name = 'dashboard_management'

urlpatterns = [

    # students info
    path(
        'onlineadmission/',
        views.OnlineAdmissionProcess.as_view(),
        name='online_admission'
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


]