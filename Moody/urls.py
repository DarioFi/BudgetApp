from django.urls import path, include

urlpatterns = [
    path("home/", lambda x: 1, name="moody home"),
    path("api/ajax/", include("Moody.api.ajax_urls")),
    path("api/rest/", include("Moody.api.rest_urls")),
]
