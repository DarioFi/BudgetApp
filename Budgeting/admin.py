from django.contrib import admin
# Register your models here.
from django.contrib.admin import DateFieldListFilter

from .models import Account, CategoryExpInc, Transaction


# todo: add good filter

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_full', 'timeDate', 'balance', 'category', 'account', 'description')
    list_filter = ('user_full', ('timeDate', DateFieldListFilter))
    ordering = ('-timeDate',)
    search_fields = ['description']


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_full', 'name', 'balance', 'starting_balance', 'created_on')

    list_filter = ('user_full',)

    ordering = ('user_full',)


class CategoryExpIncAdmin(admin.ModelAdmin):
    list_display = ('user_full', 'name', 'balance', 'created_on')

    list_filter = ('user_full',)

    ordering = ('user_full',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(CategoryExpInc, CategoryExpIncAdmin)
