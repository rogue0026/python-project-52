from django.urls import path

from task_manager.users import views

urlpatterns = [
    path(
        "create/",
        views.UserRegistrationView.as_view(),
        name="registration_view",
    ),

    path(
        "<int:pk>/update/",
        views.UpdateUserView.as_view(),
        name="users_update_view",
    ),

    path(
        "<int:pk>/delete/",
        views.DeleteUserView.as_view(),
        name="users_delete_view",
    ),

    path(
        "",
        views.UserListView.as_view(),
        name="users_list_view",
    ),
]
