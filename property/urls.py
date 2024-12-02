from django.urls import path
from property.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("sign-up/", sign_up_view, name="sign_up"),
    path("sign-up-success/", sign_up_success, name="sign_up_success"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="sign_up"), name="logout"),
    path('admin/approve-user/<int:user_id>/', approve_user, name="approve_user")
]