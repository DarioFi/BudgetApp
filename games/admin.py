from django.contrib import admin

# Register your models here.

from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'players', 'created_on')
    list_filter = ('players',)
    ordering = ('-created_on',)
    search_fields = ['name']


admin.site.register(Room, RoomAdmin)
