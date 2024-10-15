from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig

from .views import RegisterView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("catalog:home")), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
