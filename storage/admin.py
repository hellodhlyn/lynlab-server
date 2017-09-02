from django.contrib import admin

from storage.models import Object


class ObjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type', 'file', 'uploader', 'created_at', 'modified_at']
    list_editable = ['content_type']
    ordering = ['-modified_at']


admin.site.register(Object, ObjectAdmin)
