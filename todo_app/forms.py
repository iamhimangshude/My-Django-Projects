from django import forms

from todo_app.models import Tasks, Category


class TasksAddForm(forms.ModelForm):
    cat_name = forms.ModelChoiceField(
        queryset=Category.objects.all(), label="Select Category", required=False
    )
    is_starred = forms.BooleanField(label="Star Task", required=False)

    class Meta:
        model = Tasks
        exclude = ["is_completed"]
        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
