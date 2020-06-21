from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'last_login')
    list_filter = ('last_login', 'is_superuser', 'is_staff')
    ordering = ('id',)
    search_fields = ('username',)

admin.site.register(User, CustomUserAdmin)
