from django import forms

from todo_app.models import Tasks, Category


class TasksAddForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = "__all__"


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
