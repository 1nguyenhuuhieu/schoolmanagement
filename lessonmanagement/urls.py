
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('profile/', views.profile, name="profile"),
    path('lessons/', views.alllessons, name="alllessons"),
    path('lessons/<int:schoolyear>/', views.lessons_schoolyear, name="lessons_schoolyear"),

    path('lessons/empty/', views.emptylesson, name="emptylesson"),
    
    path('lessons/<str:subject>/<int:level>/', views.lessons_subject_level, name="lessons_subject_level"),
    path('lessons/<str:subject>/<int:level>/<str:title>/', views.lesson_classyear, name="lesson_classyear"),
    path('lesson/<int:id>/', views.lesson, name="lesson"),
    path('lesson/edit/<int:lesson_id>/', views.edit_lesson, name="edit_lesson"),
    path('lesson/add/', views.addlesson, name="addlesson"),
    path('lessons/add/<str:subject>/<int:level>/', views.add_lesson_subject_level, name="add_lesson_subject_level"),
    path('lessons/add/error/', views.no_permisson_add_lesson, name = 'no_permisson_add_lesson'),
    # lịch báo giảng
    
    
    path('schedule/<int:year>/<int:week>/', views.schedule, name = 'schedule'),
    path('emptyschedule/', views.emptyschedule, name = 'emptyschedule'),

    
    
    path('schedule/add/', views.add_schedule, name = 'add_schedule'),
    path('schedule/add/<int:lesson_id>/', views.add_lesson_schedule, name = 'add_lesson_schedule'),

    path('teacher/<int:teacher_id>/', views.teacher, name='teacher'),



    
] 
