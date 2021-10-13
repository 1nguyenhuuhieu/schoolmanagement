from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *
from django import forms

class SubjectClassyearForm(forms.ModelForm):
    class Meta:
        model = SubjectClassyear
        fields = ['schoolyear','teacher','subject', 'classyear','startdate','enddate','is_active']
    def clean(self):
        # kiểm tra đã chọn đúng lớp tương ứng môn học
        classyears = self.cleaned_data.get('classyear')
        subject = self.cleaned_data.get('subject')
        for classyear in classyears:
            if classyear.class_level != subject.level:
                raise ValidationError("Chọn lớp học tương ứng với môn học")
        return self.cleaned_data


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


class SubjectDetailInline(admin.TabularInline):
    model = SubjectDetail
    extra = 4

class ClassyearResource(resources.ModelResource):
    class Meta:
        model = Classyear

class LessonScheduleResource(resources.ModelResource):
    class Meta:
        model = LessonSchedule
        fields = ('id', 'classyear', 'classyear__startyear__start_date','classyear__title','week','session', 'order_schedule', 'teach_date_schedule'  )
class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
class SchoolyearResource(resources.ModelResource):
    class Meta:
        model = Schoolyear

class SubjectLessonResource(resources.ModelResource):
    class Meta:
        model = SubjectLesson
        fields = ('id', 'subject', 'subject__subject__title','subject__level', 'number_lesson', 'title')
        

class SubjectDetailResource(resources.ModelResource):
    class Meta:
        model = SubjectDetail
        fields = ('id', 'subject', 'subject__title', 'level', 'total_lesson' ,'week_lesson')
class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher



@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('title', )
    exclude = ('subject_slug',)
    inlines = [SubjectDetailInline, SubjectManagerInline ]
    resource_class = SubjectResource
  
@admin.register(SubjectLesson)
class SubjectLesson(ImportExportModelAdmin):
    list_filter = ('subject',)
    list_display = ('subject', 'number_lesson','title')
    resource_class = SubjectLessonResource


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


@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    list_display = ('__str__','id', 'main_subject', 'is_work')
    list_filter = ('main_subject', 'is_work')
    inlines = [ClassyearManagerInline, SubjectManagerInline, SubjectClassyearInline]
    resource_class = TeacherResource

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    date_hierarchy = 'upload_time'
    list_filter = ('subject', 'teacher__lastname','status','checker')

@admin.register(LessonSchedule)
class LessonScheduleAdmin(ImportExportModelAdmin):
    resource_class = LessonScheduleResource
   

@admin.register(SubjectClassyear)
class SubjectClassyearAdmin(admin.ModelAdmin):
    list_display = ('teacher','subject', 'classyear_list', 'schoolyear','is_active')
    list_filter = ('classyear', 'subject__subject__title', 'schoolyear', 'is_active')
    form = SubjectClassyearForm

@admin.register(SchoolManager)
class SchoolManagerAdmin(admin.ModelAdmin):
    pass

@admin.register(Schoolyear)
class SchoolyearAdmin(ImportExportModelAdmin):
    list_display = ('__str__','is_active', 'school')
    resource_class = SchoolyearResource

@admin.register(SubjectDetail)
class SubjectDetailAdmin(ImportExportModelAdmin):

    resource_class = SubjectDetailResource
