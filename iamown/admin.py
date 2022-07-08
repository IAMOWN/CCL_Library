from django.contrib import admin

from .models import (
    Task,
    ServiceGroup,
    LEE,
    PEeP,
    Audience,
)

admin.site.register(Task)
admin.site.register(ServiceGroup)
admin.site.register(LEE)
admin.site.register(PEeP)
admin.site.register(Audience)
