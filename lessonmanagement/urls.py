
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('lessondashboard/', views.lessondashboard, name="lessondashboard"),
    path('lessons/', views.alllessons, name="alllessons"),
    path('lessons/empty/', views.emptylesson, name="emptylesson"),
    path('lessons/<str:subject>/<int:level>/', views.lessons_subject_level, name="lessons_subject_level"),
    path('lessons/<str:subject>/<int:level>/<str:title>/', views.lesson_classyear, name="lesson_classyear"),
    path('lesson/<int:id>/', views.lesson, name="lesson"),
    path('lesson/add/', views.addlesson, name="addlesson"),


    
] 
