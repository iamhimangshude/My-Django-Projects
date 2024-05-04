from django.urls import path

from file_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.file_view, name="file-view"),
]
