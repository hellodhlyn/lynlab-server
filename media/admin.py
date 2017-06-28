from django.contrib import admin

from media.models import Media


class MediaAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_editable = ['title']
    list_display_links = None
    search_fields = ['title']
    ordering = ['title']


admin.site.register(Media, MediaAdmin)
