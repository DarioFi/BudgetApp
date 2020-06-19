from django.contrib import admin

# Register your models here.
from .models import Account, CategoryExpInc, Transaction

# todo: add good filter

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user_full', 'timeDate', 'balance', 'category', 'account', 'description')

    list_filter = ('user_full', 'timeDate')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('user_full', 'name', 'balance', 'starting_balance', 'created_on')

    list_filter = ('user_full',)


class CategoryExpIncAdmin(admin.ModelAdmin):
    list_display = ('user_full', 'name', 'exchange', 'created_on')

    list_filter = ('user_full',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(CategoryExpInc, CategoryExpIncAdmin)
