from django.urls import path

from todo_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:slug>", views.home, name="home"),
    path("create-category/", views.create_category, name="create-category"),
    path("create-task/", views.create_task, name="create-task"),
    path("edit-task/<uuid:task_id>", views.edit_task, name="edit-task"),
    path("complete-task/<uuid:task_id>", views.complete_task, name="complete-task"),
    path("star-task/<uuid:task_id>", views.star_task, name="star-task"),
    path("delete-task/<uuid:task_id>", views.delete_task, name="delete-task"),
    path(
        "delete-category/<uuid:category_id>",
        views.delete_category,
        name="delete-category",
    ),
]
