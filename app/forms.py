from django import forms
from .models import Tasks, Tags


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'done', 'tags']


class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['name']