from .models import Article
from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "is_public"]
    list_editable = ["is_public"]

admin.site.register(Article, ArticleAdmin)
