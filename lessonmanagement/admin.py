from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(GroupSubject)
admin.site.register(SubjectManager)
admin.site.register(GroupSubjectManager)
admin.site.register(ClassYear)
admin.site.register(ClassYearManager)



