from django.urls import path

from .views import (
    TagList,
)

urlpatterns = [
    # Tasks
    path('tasks/', TagList.as_view(), name='tasks'),
]