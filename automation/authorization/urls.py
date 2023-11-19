from django.urls import path
from .views import login_view,signup_view,base_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("base_home/", base_view, name="base_home")
]