from django.contrib import admin

from .models import (
    Task,
    ServiceGroup,
    LEE,
)

admin.site.register(Task)
admin.site.register(ServiceGroup)
admin.site.register(LEE)
