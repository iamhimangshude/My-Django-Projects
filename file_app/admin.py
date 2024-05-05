from django.contrib import admin

from file_app.models import File, Folder

# Register your models here.
admin.site.register(File)
admin.site.register(Folder)
