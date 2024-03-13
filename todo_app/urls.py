from django.urls import path

from todo_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:slug>", views.home, name="home"),
    path("create-category/", views.create_category, name="create-category"),
    path("create-task/", views.create_task, name="create-task"),
]
