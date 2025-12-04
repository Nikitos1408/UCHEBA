from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("accounts/signup/", views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]