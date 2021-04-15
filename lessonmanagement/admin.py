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

admin.site.register(ClassYearManager)
admin.site.register(Lesson)
admin.site.register(SubjectClassYear)
admin.site.register(LessonClassYear)



