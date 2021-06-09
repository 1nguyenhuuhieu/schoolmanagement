from django import forms
from .models import *

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('avatar',)



class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()