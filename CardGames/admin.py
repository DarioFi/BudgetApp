from django.contrib import admin

# Register your models here.
from .models import match_scopa, match_invite

admin.site.register([match_invite, match_scopa])