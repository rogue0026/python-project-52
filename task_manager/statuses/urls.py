from django.urls import path
from task_manager.statuses.views import (
    StatusesListView,
    CreateStatusView,
    UpdateStatusView,
    DeleteStatusView,
)

urlpatterns = [
    path('', StatusesListView.as_view(), name="statuses_list_view"),
    path('create/', CreateStatusView.as_view(), name='statuses_create_view'),
    path('<int:pk>/update/', UpdateStatusView.as_view(), name="statuses_update_view"),
    path('<int:pk>/delete/', DeleteStatusView.as_view(), name="statuses_delete_view"),
]