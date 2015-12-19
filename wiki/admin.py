# -*- coding: utf-8 -*-

from django.contrib import admin

from wiki.models import Article, ModifyHistory

class WikiContentAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_editable = ['title']
    search_fields = ['title']
    ordering = ['title']

class WikiHistoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'editor', 'timestamp']
    search_fields = ['title', 'editor']
    ordering = ['title', 'timestamp']

admin.site.register(Article, WikiContentAdmin)
admin.site.register(ModifyHistory, WikiHistoryAdmin)