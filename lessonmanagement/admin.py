from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Teacher)

class TeacherAdmin(admin.ModelAdmin):
    # fields = ('firstname', 'lastname','is_work')
    list_display = ('firstname', 'lastname','main_subject','is_work')
    list_filter = ('is_work','main_subject')
admin.site.register(Subject)
admin.site.register(GroupSubject)
admin.site.register(SubjectManager)
admin.site.register(GroupSubjectManager)
admin.site.register(ClassYear)
admin.site.register(ClassYearManager)
admin.site.register(Lesson)



