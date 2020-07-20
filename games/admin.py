from django.contrib import admin

# Register your models here.

from games.database.models import GameRoom


class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on')
    list_filter = ('players',)
    ordering = ('-created_on',)
    search_fields = ['name']


admin.site.register(GameRoom, RoomAdmin)

# todo: register Cactus games or something similar