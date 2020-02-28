from django.contrib import admin

# Register your models here.
from .models import Account, CategoryExpInc, Transaction

admin.site.register([Account, CategoryExpInc, Transaction])