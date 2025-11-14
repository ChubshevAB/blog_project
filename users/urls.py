from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserRegistrationView, UserListView, UserDetailView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", obtain_auth_token, name="user-login"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
