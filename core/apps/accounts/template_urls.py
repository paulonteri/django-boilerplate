from apps.accounts.views import home, signup
from django.conf.urls import url
from django.urls import include, path

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("home", home, name="home"),
    url(r"^signup/$", signup, name="signup"),
    path("", home, name="index"),
]
