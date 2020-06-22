from django.contrib import admin

# Register your models here.
from .models import moody_record


class moodyRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'data')

    list_filter = ('user',)

    ordering = ('user',)


admin.site.register(moody_record, moodyRecordAdmin)
