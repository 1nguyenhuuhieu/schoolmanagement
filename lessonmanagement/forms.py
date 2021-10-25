from django.forms import ModelForm
from django import forms
from .models import LectureFile

class LectureFileForm(ModelForm):
    class Meta:
        model = LectureFile
        fields = ['title', 'file', 'user']
        widgets = {'user': forms.HiddenInput()}

class CheckForm(forms.Form):
    pwd = forms.PasswordInput()