from django.contrib import admin
from .models import *

# Register your models here.
class SubjectClassYearInline(admin.TabularInline):
    model = SubjectClassYear

class ClassYearManagerInline(admin.TabularInline):
    model = ClassYearManager



@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    # date_hierarchy = 'birth_date'
    list_display = ['lastname','firstname','user',  'main_subject', 'is_work']
    list_filter  = ('main_subject','is_work')
    inlines = [SubjectClassYearInline]
    

@admin.register(ClassYear)
class ClassYearAdmin(admin.ModelAdmin):

    list_display = ['class_title_year', 'startyear']
    # @admin.display(description='ClassYearTitle')

    list_filter  = ('title',)

    inlines = [SubjectClassYearInline, ClassYearManagerInline]

# admin.site.register(Subject)
# admin.site.register(GroupSubject)
# admin.site.register(SubjectTeacher)
# admin.site.register(GroupSubjectManager)

# admin.site.register(ClassYearManager)
# admin.site.register(Lesson)
# admin.site.register(SubjectClassYear)
# admin.site.register(LessonClassYear)



