from django.urls import path

from .views import (
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
    TaskDelete,
    TaskCompletedList,
    TaskLibraryList,
    TaskLibraryDetail,
    TaskLibraryCompletedList,
    TaskLibraryCreate,
    TaskLibraryDelete,
    ServiceGroupList,
    ServiceGroupDetail,
    ServiceGroupCreate,
    ServiceGroupUpdate,
    ServiceGroupDelete,
)

urlpatterns = [
    # Tasks
    path('tasks/', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task_create/', TaskCreate.as_view(), name='task-create'),
    path('task_update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('tasks/completed/', TaskCompletedList.as_view(), name='tasks-completed'),
    path('task_delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    # Library Tasks
    path('tasks/library/', TaskLibraryList.as_view(), name='tasks-library'),
    path('task/library/<int:pk>/', TaskLibraryDetail.as_view(), name='task-library'),
    path('task_create/library/', TaskLibraryCreate.as_view(), name='task-create-library'),
    path('tasks/completed/library/', TaskLibraryCompletedList.as_view(), name='tasks-completed-library'),
    path('task_delete/library/<int:pk>/', TaskLibraryDelete.as_view(), name='task-delete-library'),

    # Service Groups
    path('service_groups/', ServiceGroupList.as_view(), name='service-groups'),
    path('service_group/<int:pk>/', ServiceGroupDetail.as_view(), name='service-group'),
    path('service_group_create/', ServiceGroupCreate.as_view(), name='service-group-create'),
    path('service_group_update/<int:pk>/', ServiceGroupUpdate.as_view(), name='service-group-update'),
    path('service_group_delete/<int:pk>/', ServiceGroupDelete.as_view(), name='service-group-delete'),
]