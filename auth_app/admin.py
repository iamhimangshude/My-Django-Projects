from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_app.models import UserModel
# Register your models here.

@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    model = UserModel
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser")

    fieldsets = (
        ('Profile', {'fields': ('first_name','last_name','email', 'password')}),
        (
            "Permissions",
            {
                'fields':(
                    'user_permissions',
                    'groups',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                )
            }
        ),
        (
            'Dates and Other data',
            {
                'fields':(
                    'date_of_birth',
                    'last_login',
                    'date_joined',
                    'otp',
                    'otp_expiry',
                )
            }
        )
    )

    add_fieldsets = (  # fieldsets for adding a new user from admin site.
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    search_fields = ['email']
    ordering = ['email']


admin.site.site_title = 'Blog Administration'
admin.site.site_header = 'Blog Administration'