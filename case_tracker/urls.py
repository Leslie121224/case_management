from django.urls import path
from .views import register, case_list, case_detail, add_case, edit_case
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    # 案件管理相關 URL
    path("cases/", case_list, name="case_list"),
    path("cases/<int:case_id>/", case_detail, name="case_detail"),
    path("cases/add/", add_case, name="add_case"),
    path("cases/<int:case_id>/edit/", edit_case, name="edit_case"),
]
