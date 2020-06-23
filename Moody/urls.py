from django.urls import path, include

urlpatterns = [
    path("home/", lambda x: 1, name="moody home")
]