from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers

from .api import (
    GroupAPI,
    LoginAPI,
    PermissionAPI,
    RegisterAPI,
    UpdateUserAPI,
    UserAPI,
)

router = routers.DefaultRouter()

router.register("update", UpdateUserAPI, "UpdateUserAPI")

urlpatterns = [
    path("user", UserAPI.as_view()),
    #
    path("register", RegisterAPI.as_view()),
    #
    path("login", LoginAPI.as_view()),
    path("logout", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall", knox_views.LogoutAllView.as_view(), name="knox_logout"),
    #
    path("roles/groups", GroupAPI.as_view()),
    path("roles/permissions", PermissionAPI.as_view()),
    #
    path("", include(router.urls)),
    # path('', include('knox.urls')),
]
