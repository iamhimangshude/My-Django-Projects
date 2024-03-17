from django.http import HttpResponseRedirect
from django.shortcuts import render

from todo_app.forms import CategoryAddForm, TasksAddForm
from todo_app.models import Tasks, Category

# Create your views here.


def home(request, slug=None):
    category_data = Category.objects.all()
    context = {}
    context["categories"] = category_data
    context["tasks"] = []
    context["slug"] = None
    if "slug" in request.session:
        request.session.pop("slug")
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
        request.session["slug"] = slug

    if slug == "completed":
        task_list = Tasks.objects.filter(is_completed=True)
        context["tasks"] = task_list
        context["slug"] = slug
        request.session["slug"] = slug

    if slug == "starred":
        task_list = Tasks.objects.filter(is_starred=True)
        context["tasks"] = task_list
        context["slug"] = slug
        request.session["slug"] = slug
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

    # Main form part
    form = TasksAddForm()
    context["form"] = form
    if request.method == "POST":
        form = TasksAddForm(request.POST)
        context["form"] = form
        if form.is_valid():
            form.save()
            redirect_to = form.cleaned_data["cat_name"]
            return HttpResponseRedirect(f"/{redirect_to}")

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
            redirect_to = Category.objects.get(
                cat_name=form.cleaned_data["cat_name"]
            ).cat_id
            return HttpResponseRedirect(f"/{redirect_to}")

    return render(
        request,
        "todo_app/create_category.html",
        context,
    )


def edit_task(request, task_id):
    category_data = Category.objects.all()
    context = {}
    context["categories"] = category_data
    context["tasks"] = []
    for items in category_data:
        context["tasks"].extend(
            Category.objects.get(cat_name=items).category.filter(is_completed=False)
        )

    # Main form part
    task = Tasks.objects.get(task_id=task_id)
    form = TasksAddForm(instance=task)
    context["form"] = form
    if request.method == "POST":
        form = TasksAddForm(request.POST, instance=task)
        context["form"] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/{request.session.get('slug')}")
    return render(request, "todo_app/edit_task.html", context)


def is_completed(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return HttpResponseRedirect(f"/{request.session.get('slug')}")


def delete_task(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    task.delete()
    if request.session.get("slug") is not None:
        return HttpResponseRedirect(f"/{request.session.get('slug')}")
    return HttpResponseRedirect("/")


def star_task(request, task_id):
    task = Tasks.objects.get(task_id=task_id)
    task.is_starred = not task.is_starred
    task.save()
    if request.session.get("slug") is not None:
        return HttpResponseRedirect(f"/{request.session.get('slug')}")
    return HttpResponseRedirect("/")
