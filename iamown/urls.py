from django.urls import path

from .views import (
    test
)

urlpatterns = [
    # Tasks
    path('tasks/', test, name='tasks'),
]