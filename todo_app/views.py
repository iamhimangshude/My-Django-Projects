from django.shortcuts import render

from todo_app.models import Tasks, Category

# Create your views here.


def home(request, slug=None):
    tasks_data = Tasks.objects.all()
    category_data = Category.objects.all()
    context = {}
    context["tasks"] = tasks_data
    context["categories"] = category_data
    context["cat_name"] = slug

    if slug:
        print(slug)  # DEBUG PRINT
        all_tasks = Category.objects.get(cat_name__contains=slug).category.all()
        context["tasks"] = all_tasks
        context["cat_name"] = slug or None

    return render(request, "todo_app/home.html", context)
