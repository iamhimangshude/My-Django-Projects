from django.urls import path

from file_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("folder/<uuid:folder_id>/", views.folder_view, name="folder-view"),
    path("file/<uuid:file_id>/", views.file_view, name="file-view"),
    path("upload/", views.file_upload_view, name="file-upload-view"),
]
