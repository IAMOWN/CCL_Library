from django.urls import path

from .views import (
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
)

urlpatterns = [
    # Tasks
    path('tasks/', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task_create/', TaskCreate.as_view(), name='task-create'),
    path('task_update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task_delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
]