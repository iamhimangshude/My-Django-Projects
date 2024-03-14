from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from todo_app.forms import CategoryAddForm, TasksAddForm
from todo_app.models import Tasks, Category

# Create your views here.


def home(request, slug=None):
    category_data = Category.objects.all()
    context = {}
    context["categories"] = category_data
    context["tasks"] = []
    context["slug"] = None
    for items in category_data:
        context["tasks"].extend(
            Category.objects.get(cat_name=items).category.filter(is_completed=False)
        )

    if slug != None and slug != "completed" and slug != "starred":
        task_list = Category.objects.get(cat_id=slug).category.filter(
            is_completed=False
        )
        context["tasks"] = task_list
        context["slug"] = Category.objects.get(cat_id=slug).cat_name

    if slug == "completed":
        task_list = Tasks.objects.filter(is_completed=True)
        context["tasks"] = task_list
        context["slug"] = slug

    if slug == "starred":
        task_list = Tasks.objects.filter(is_starred=True)
        context["tasks"] = task_list
        context["slug"] = slug
    return render(request, "todo_app/home.html", context)


def create_task(request):
    category_data = Category.objects.all()
    context = {}
    context["categories"] = category_data
    context["tasks"] = []
    for items in category_data:
        context["tasks"].extend(
            Category.objects.get(cat_name=items).category.filter(is_completed=False)
        )
    context["slug"] = None
    form = TasksAddForm()
    context["form"] = form
    context["create"] = True
    if request.method == "POST":
        form = TasksAddForm(request.POST)
        context["form"] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home"))

    return render(request, "todo_app/create_task.html", context)


def create_category(request):
    category_data = Category.objects.all()
    context = {}
    context["categories"] = category_data
    context["tasks"] = []
    for items in category_data:
        # print(Category.objects.get(cat_name=items).category.all())
        context["tasks"].extend(Category.objects.get(cat_name=items).category.all())

    # Main category part
    form = CategoryAddForm()
    context["form"] = form
    if request.method == "POST":
        form = CategoryAddForm(request.POST)
        context["form"] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home"))

    return render(
        request,
        "todo_app/create_category.html",
        context,
    )


def edit_task(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    form = TasksAddForm(instance=task)
    if request.method == "POST":
        form = TasksAddForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home"))
    return render(request, "todo_app/create_task.html", {"form": form, "create": False})


def is_completed(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return HttpResponseRedirect(reverse("home"))


def delete_task(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    task.delete()
    return HttpResponseRedirect(reverse("home"))


def star_task(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    task.is_starred = not task.is_starred
    task.save()
    return HttpResponseRedirect(reverse("home"))
