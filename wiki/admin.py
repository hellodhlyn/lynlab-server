# -*- coding: utf-8 -*-

from django.contrib import admin

from wiki.models import Article


class WikiContentAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_editable = ['title']
    search_fields = ['title']
    ordering = ['title']

admin.site.register(Article, WikiContentAdmin)