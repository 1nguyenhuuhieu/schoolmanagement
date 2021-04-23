from django.contrib import admin
from .models import *

class SubjectTeacherInline(admin.TabularInline):
    model = SubjectTeacher
    extra = 2
class SubjectClassyearInline(admin.TabularInline):
    model = SubjectClassyear
class ClassyearManagerInline(admin.TabularInline):
    model = ClassyearManager
    extra = 1

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'group' )
    list_filter = ('group', )
    exclude = ('subject_slug',)
    inlines = [SubjectTeacherInline, SubjectClassyearInline]

@admin.register(GroupSubject)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ( 'title', )
    
@admin.register(SubjectTeacher)
class SubjectTeacherAdmin(admin.ModelAdmin):
    pass
@admin.register(ClassyearManager)
class ClassyearManagerAdmin(admin.ModelAdmin):
    pass
@admin.register(GroupSubjectManager)
class GroupSubjectManagerAdmin(admin.ModelAdmin):
    pass
@admin.register(Classyear)
class ClassyearAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_learning', 'class_level')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'main_subject', 'is_work')
    list_filter = ('main_subject', 'is_work')
    inlines = [ClassyearManagerInline, SubjectTeacherInline, SubjectClassyearInline]
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
@admin.register(LessonClassyear)
class LessonClassyearAdmin(admin.ModelAdmin):
    pass
@admin.register(SubjectClassyear)
class SubjectClassyearAdmin(admin.ModelAdmin):
    pass