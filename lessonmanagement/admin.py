from django.contrib import admin
from .models import *

# Register your models here.
class SubjectClassYearInline(admin.TabularInline):
    model = SubjectClassYear




@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [SubjectClassYearInline]


@admin.register(ClassYear)
class ClassYearAdmin(admin.ModelAdmin):

    list_display = ['class_title_year', 'startyear']
    # @admin.display(description='ClassYearTitle')

    inlines = [SubjectClassYearInline]

# admin.site.register(Subject)
# admin.site.register(GroupSubject)
# admin.site.register(SubjectTeacher)
# admin.site.register(GroupSubjectManager)

# admin.site.register(ClassYearManager)
# admin.site.register(Lesson)
# admin.site.register(SubjectClassYear)
# admin.site.register(LessonClassYear)



