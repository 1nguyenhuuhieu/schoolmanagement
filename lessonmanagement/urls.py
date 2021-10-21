
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('profile/', views.profile, name="profile"),
    path('profile/<int:teacher_id>/', views.profile_detail, name="profile_detail"),
    path('lessons/', views.lessons, name='lessons'),
    path('lessons/<int:schoolyear>/', views.lessons, name="lessons_schoolyear"),
    
    path('lessons/week/', views.week_lessons, name='now_week_lessons'),
    path('lessons/week/<int:url_week>/', views.week_lessons, name='week_lessons'),

    path('lessons/empty/', views.emptylesson, name="emptylesson"),
    path('lesson/open/<int:id>/', views.open_lesson, name="open_lesson"),
    path('lesson/<int:id>/', views.lesson, name="lesson"),
    path('lesson/edit/<int:lesson_id>/', views.edit_lesson, name="edit_lesson"),
    path('lesson/add/', views.addlesson, name="addlesson"),
    path('lesson/add/<int:url_week>/', views.addlesson, name="addlesson_week"),
    path('lessons/add/<str:subject>/', views.add_lesson_subject, name="add_lesson_subject"),
    path('lessons/add/<str:subject>/<int:url_week>/', views.add_lesson_subject, name="add_lesson_subject_week"),
    path('lessons/add/error/', views.no_permisson_add_lesson, name = 'no_permisson_add_lesson'),
    path('lessons/<str:subject>/', views.lessons_subject, name="lessons_subject"),

    # lịch báo giảng
    path('schedule/add/', views.add_schedule, name = 'add_schedule'),
    path('schedule/add/<int:lesson_id>/', views.add_lesson_schedule, name = 'add_lesson_schedule'),
    path('schedule/<str:username_url>/', views.schedule, name = 'now_schedule'),
    path('schedule/<str:username_url>/<int:url_week>/', views.schedule, name = 'schedule'),

    # DUYệt GIÁO ÁN
     path('checklessons/<int:year>/<str:subject>/', views.check_lessons_subject, name='check_lessons_subject'),
     path('checklesson/<int:lesson_id>/', views.check_lesson, name='check_lesson'),
     path('checklesson/open/<int:lesson_id>/', views.check_open_lesson, name='check_open_lesson'),
    # THỐNG KÊ LỊCH BÁO GIẢNG
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<int:week>/', views.dashboard, name='dashboard_week'),
    path('emptyschedule/', views.emptyschedule, name = 'emptyschedule'),

    path('teacher/<int:teacher_id>/', views.teacher, name='teacher'),

    #Tải lên file
    path('upload/', views.upload_file, name='upload'),

    path('bb/', views.bb, name='bb'),

] 
