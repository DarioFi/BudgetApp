from django.contrib import admin

# Register your models here.
from .models import match_invitation, match_scopa, games_notification

admin.site.register([match_invitation, match_scopa, games_notification])