from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Import your custom user model

# Define a custom UserAdmin to display additional fields
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'mobile', 'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'mobile')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'mobile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register the custom user model with the customized UserAdmin
admin.site.register(User, CustomUserAdmin)
