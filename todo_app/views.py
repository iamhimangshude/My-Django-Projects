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
    for items in category_data:
        # print(Category.objects.get(cat_name=items).category.all())
        context["tasks"].extend(Category.objects.get(cat_name=items).category.all())

    if slug != None:
        task_list = Category.objects.get(cat_name=slug).category.all()
        context["tasks"] = task_list
    return render(request, "todo_app/home.html", context)


def create_task(request):
    form = TasksAddForm()
    if request.method == "POST":
        form = TasksAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home"))

    return render(request, "todo_app/create_task.html", {"form": form})


def create_category(request):
    category_data = Category.objects.all()
    context = {}
    context["categories"] = category_data
    context["tasks"] = []
    for items in category_data:
        # print(Category.objects.get(cat_name=items).category.all())
        context["tasks"].extend(Category.objects.get(cat_name=items).category.all())
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
