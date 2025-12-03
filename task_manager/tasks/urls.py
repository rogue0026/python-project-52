from django.urls import path

from task_manager.tasks.views import (
    CreateTaskView,
    DeleteTaskView,
    DetailsTaskView,
    TasksListView,
    UpdateTaskView,
)

urlpatterns = [
    path("", TasksListView.as_view(), name="tasks_list_view"),
    path("create/", CreateTaskView.as_view(), name="tasks_create_view"),
    path("<int:pk>/update/", UpdateTaskView.as_view(), name="tasks_update_view"),
    path("<int:pk>/delete/", DeleteTaskView.as_view(), name="tasks_delete_view"),
    path("<int:pk>/", DetailsTaskView.as_view(), name="tasks_details_view"),
]