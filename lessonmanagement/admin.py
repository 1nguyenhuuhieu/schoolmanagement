from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subject)
admin.site.register(GroupSubject)
admin.site.register(SubjectTeacher)
admin.site.register(GroupSubjectManager)
admin.site.register(ClassYear)
admin.site.register(ClassYearManager)
admin.site.register(Lesson)
admin.site.register(SubjectClassYear)
admin.site.register(LessonClassYear)



