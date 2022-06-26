from django.contrib import admin

from .models import (
    Task,
    ServiceGroup,
)

admin.site.register(Task)
admin.site.register(ServiceGroup)
