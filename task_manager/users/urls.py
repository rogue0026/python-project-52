from django.urls import path
from task_manager.users import views


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login_view"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path("create/", views.UserRegistrationView.as_view(), name="registration_view"),
    path("<int:pk>/update/", views.UpdateUserView.as_view(), name="update_view"),
    path("<int:pk>/delete/", views.DeleteUserView.as_view(), name="delete_view"),
    path("", views.UserListView.as_view(), name="users_list_view"),
]
