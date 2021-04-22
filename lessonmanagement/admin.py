from django.contrib import admin
from .models import *

# Register your models here.
class SubjectClassYearInline(admin.TabularInline):
    model = SubjectClassYear
class ClassYearManagerInline(admin.TabularInline):
    model = ClassYearManager
class SubjectTeacherInline(admin.TabularInline):
    model = SubjectTeacher
    extra = 5

class SubjectInline(admin.TabularInline):
    model = Subject

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    # date_hierarchy = 'birth_date'
    list_display = ['fullname','main_subject','user',   'is_work']
    @admin.display()
    def fullname(self, obj):
        return '%s %s' % (obj.firstname, obj.lastname)
    list_filter  = ('main_subject','is_work')
    inlines = [SubjectTeacherInline, SubjectClassYearInline, ClassYearManagerInline]

@admin.register(ClassYear)
class ClassYearAdmin(admin.ModelAdmin):
    list_display = ['class_title_year', 'startyear','class_year_manager_name']
    @admin.display()
    def class_year_manager_name(self, obj):
        class_year_manager = ClassYearManager.objects.filter(class_year_id = obj.id)

        if class_year_manager:
            for i in class_year_manager:
                if i.enddate:
                    return "Chưa có Giáo viên chủ nhiệm"
                else:
                    return i.teacher
        else:
            return "Chưa có Giáo viên chủ nhiệm"
    list_filter  = ('title',)
    inlines = [SubjectClassYearInline, ClassYearManagerInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [SubjectTeacherInline]
    list_display = ['title','group']
    list_filter = ('group',)
  




@admin.register(SubjectTeacher)
class SubjectTeacher(admin.ModelAdmin):
    pass

@admin.register(GroupSubject)
class GroupSubject(admin.ModelAdmin):
    pass


admin.site.register(GroupSubjectManager)

@admin.register(LessonClassYear)
class LessonClassYear(admin.ModelAdmin):
    pass
@admin.register(Lesson)
class Lesson(admin.ModelAdmin):
    empty_value_display = '---1231232'

@admin.register(SubjectClassYear)

class SubjectClassYear(admin.ModelAdmin):
    date_hierarchy = 'startdate'
    list_display = ['__str__','is_teach_now','subject_name', 'teacher_name', 'startdate' , 'enddate']

    list_filter = ('subject__title', 'is_teach_now', 'teacher')

    @admin.display()
    def subject_name(self, obj):
        return ("%s %s %s" % (obj.subject.title, obj.classyear.class_level(), obj.classyear.get_title_display() ))
    def teacher_name(self, obj):
        return obj.teacher.full_name()



@admin.register(SchoolManager)
class SchoolManager(admin.ModelAdmin):
    pass


@admin.register(School)
class School(admin.ModelAdmin):
    pass




