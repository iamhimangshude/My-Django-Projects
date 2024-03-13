from django.contrib import admin

from todo_app.models import Tasks, Category

# Register your models here.
admin.site.register(Tasks)
admin.site.register(Category)

admin.site.site_title = "ToDo Administration"
admin.site.index_title = "Sites and Control"
admin.site.site_header = "ToDo Admin"
