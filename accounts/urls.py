from django.urls import path
from .views import *

urlpatterns = [
    path("",register_view),
    path("login/",login_view),
    path("logout/",logout_view),
    path("refresh/",refresh_token_view),
    path("profile/",profile_view),
    path("assign-role/<int:pk>/",assign_role_view),
]
