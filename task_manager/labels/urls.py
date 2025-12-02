from django.urls import path
from task_manager.labels.views import (
    LabelListView,
    CreateLabelView,
    DeleteLabelView,
    UpdateLabelView,
)


urlpatterns = [
    path("<int:pk>/update/", UpdateLabelView.as_view(), name="labels_update_view"),
    path("<int:pk>/delete/", DeleteLabelView.as_view(), name="labels_delete_view"),
    path("create/", CreateLabelView.as_view(), name="labels_create_view"),
    path("", LabelListView.as_view(), name="labels_list_view"),
]
