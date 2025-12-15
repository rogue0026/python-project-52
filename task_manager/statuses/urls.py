from django.urls import path

from task_manager.statuses.views import (
    CreateStatusView,
    DeleteStatusView,
    StatusesListView,
    UpdateStatusView,
)

urlpatterns = [
    path(
        'create/',
        CreateStatusView.as_view(),
        name='statuses_create_view',
    ),

    path(
        '<int:pk>/update/',
        UpdateStatusView.as_view(),
        name="statuses_update_view",
    ),

    path(
        '<int:pk>/delete/',
        DeleteStatusView.as_view(),
        name="statuses_delete_view",
    ),

    path(
        '',
        StatusesListView.as_view(),
        name="statuses_list_view",
    ),
]