from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'last_login_action')
    list_filter = ('last_login', 'is_superuser', 'is_staff', 'last_login_action')
    ordering = ('id',)
    search_fields = ('username',)

admin.site.register(User, CustomUserAdmin)
