from django.urls import path
from .views import home, add_note, edit_note, delete_note

urlpatterns = [
    path('', home, name='home'),
    path("add-note", add_note, name='add-note'),
    path("edit-note/<int:id>", edit_note, name='edit-note'),
    path("delete-note/<int:id>", delete_note, name='delete-note'),
]
