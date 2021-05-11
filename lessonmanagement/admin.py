from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class SubjectTeacherInline(admin.TabularInline):
    model = SubjectTeacher
    extra = 2
class SubjectInline(admin.TabularInline):
    model = Subject
class SubjectClassyearInline(admin.TabularInline):
    model = SubjectClassyear
class ClassyearManagerInline(admin.TabularInline):
    model = ClassyearManager
    extra = 1

class SchoolManagerInline(admin.TabularInline):
    model = SchoolManager

class GroupSubjectManagerInline(admin.TabularInline):
    model = GroupSubjectManager


class SubjectResource(resources.ModelResource):

    class Meta:
        model = Subject



@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    inlines = [SchoolManagerInline,]
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('title', 'group' )
    list_filter = ('group', )
    exclude = ('subject_slug',)
    inlines = [SubjectTeacherInline, SubjectClassyearInline]
    resource_class = SubjectResource

@admin.register(GroupSubject)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ( 'title', )
    inlines = [SubjectInline, GroupSubjectManagerInline]
    
@admin.register(SubjectTeacher)
class SubjectTeacherAdmin(admin.ModelAdmin):
    date_hierarchy = 'startdate'
    list_display = ('subject','teacher','role', 'is_active')
    list_filter = ('subject','role', 'is_active')
@admin.register(Classyear)
class ClassyearAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_learning', 'class_level')
    inlines = [ClassyearManagerInline]    
@admin.register(ClassyearManager)
class ClassyearManagerAdmin(admin.ModelAdmin):
    pass
@admin.register(GroupSubjectManager)
class GroupSubjectManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'main_subject', 'is_work')
    list_filter = ('main_subject', 'is_work')
    inlines = [ClassyearManagerInline, SubjectTeacherInline, SubjectClassyearInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    date_hierarchy = 'upload_time'
    list_filter = ('subject', 'subject__group__title','level','teacher__lastname','status','checker')



@admin.register(LessonClassyear)
class LessonClassyearAdmin(admin.ModelAdmin):
    pass
@admin.register(SubjectClassyear)
class SubjectClassyearAdmin(admin.ModelAdmin):
    list_filter = ('classyear', 'subject__title', 'is_teach_now')

@admin.register(SchoolManager)
class SchoolManagerAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Schoolyear)
class SchoolyearAdmin(admin.ModelAdmin):
    pass

@admin.register(SubjectLesson)
class SubjectLessonAdmin(admin.ModelAdmin):
    pass

