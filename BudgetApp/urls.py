from django.contrib import admin
from django.urls import path, include

from pages.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('home/', home_view, name='home'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('budget/', include('Budgeting.urls')),
    path('games/', include('CardGames.urls')),
    path('changelog', changelog, name="changelog"),
    path('accounts/', include('allauth.urls')),
    path('moody/', include('Moody.urls')),
    path('chat/', include('chat_test.urls'))
]
