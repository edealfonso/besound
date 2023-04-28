from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.custom_users.forms import CustomUserChangeForm, CustomUserCreationForm
from solo.admin import SingletonModelAdmin

from apps.custom_users.models import CustomUser, LoginPage, RegisterPage

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {
            "fields": (
                'last_name', 
                'first_name',
                'nationality',
                'birth_date',
                "email", 
                "password", 
            )
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "groups", "user_permissions")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                'last_name', 
                'first_name',
                'nationality',
                'birth_date',
                "email", 
                "password1", 
                "password2", 
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(RegisterPage, SingletonModelAdmin)
admin.site.register(LoginPage, SingletonModelAdmin)