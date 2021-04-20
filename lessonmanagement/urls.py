
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('lessondashboard/', views.lessondashboard, name="lessondashboard"),
    path('lessons/', views.alllessons, name="alllessons"),
    path('lessons/<str:subject>/<int:level>/', views.lessons_subject_level, name="lessons_subject_level"),


    
] 
