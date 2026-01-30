from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path('login/', views.login_view, name="login" ),
    path("account/", views.account_view, name="account"),
    path(
        "account/password/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url=reverse_lazy("accounts:password_change_done"),  
        ),
        name="password_change",
    ),
    path(
        "account/password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
