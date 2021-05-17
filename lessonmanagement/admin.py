from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

class SubjectManagerInline(admin.TabularInline):
    model = SubjectManager
    extra = 1
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

class SubjectDetailInline(admin.TabularInline):
    model = SubjectDetail
    extra = 4


class ClassyearResource(resources.ModelResource):

    class Meta:
        model = Classyear

class SubjectLessonResource(resources.ModelResource):
    class Meta:
        model = SubjectLesson

class SubjectDetailResource(resources.ModelResource):
    class Meta:
        model = SubjectDetail
class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher



@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    inlines = [SchoolManagerInline,]
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'group' )
    list_filter = ('group', )
    exclude = ('subject_slug',)
    inlines = [SubjectDetailInline, SubjectManagerInline ]
  
@admin.register(SubjectLesson)
class SubjectLesson(ImportExportModelAdmin):
    list_filter = ('subject',)
    list_display = ('subject', 'number_lesson','title')
    resource_class = SubjectLessonResource

@admin.register(GroupSubject)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ( 'title', )
    
@admin.register(SubjectManager)
class SubjectManagerAdmin(admin.ModelAdmin):
    date_hierarchy = 'startdate'
    list_display = ('subject','teacher', 'is_active')
    list_filter = ('subject', 'is_active')

@admin.register(Classyear)
class ClassyearAdmin(ImportExportModelAdmin):
    list_display = ('__str__', 'is_learning', 'class_level')
    inlines = [ClassyearManagerInline]    
    resource_class = ClassyearResource

@admin.register(ClassyearManager)
class ClassyearManagerAdmin(admin.ModelAdmin):
    pass

@admin.register(GroupSubjectManager)
class GroupSubjectManagerAdmin(admin.ModelAdmin):
    pass

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    list_display = ('__str__','id', 'main_subject', 'is_work')
    list_filter = ('main_subject', 'is_work')
    inlines = [ClassyearManagerInline, SubjectManagerInline, SubjectClassyearInline]
    esource_class = TeacherResource

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    date_hierarchy = 'upload_time'
    list_filter = ('subject', 'subject__subject__group__title','teacher__lastname','status','checker')

@admin.register(LessonSchedule)
class LessonScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(SubjectClassyear)
class SubjectClassyearAdmin(admin.ModelAdmin):
    list_filter = ('classyear', 'subject__title')

@admin.register(SchoolManager)
class SchoolManagerAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Schoolyear)
class SchoolyearAdmin(admin.ModelAdmin):
    pass

@admin.register(SubjectDetail)
class SubjectLessonAdmin(ImportExportModelAdmin):
     resource_class = SubjectDetailResource

