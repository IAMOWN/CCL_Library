from django.contrib import admin

from .models import (
    Tag,
    CosmicAuthor,
    LibraryRecord,
    DiscourseSeries,
    Collection,
    CollectionOrder,
    ReadingProgress,
    LibraryObservation,
)


class CollectionOrderInlineAdmin(admin.TabularInline):
    model = CollectionOrder


class CollectionAdmin(admin.ModelAdmin):
    inlines = [CollectionOrderInlineAdmin]


admin.site.register(Tag)
admin.site.register(CosmicAuthor)
admin.site.register(LibraryRecord)
admin.site.register(DiscourseSeries)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(ReadingProgress)
admin.site.register(LibraryObservation)
