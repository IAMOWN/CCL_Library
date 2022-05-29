from django.contrib import admin

from .models import (
    Tag,
    CosmicAuthor,
    LibraryRecord,
    DiscourseSeries,
)
admin.site.register(Tag)
admin.site.register(CosmicAuthor)
admin.site.register(LibraryRecord)
admin.site.register(DiscourseSeries)
