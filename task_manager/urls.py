from django.contrib import admin
from django.urls import include, path

from task_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name="start_page"),
]
