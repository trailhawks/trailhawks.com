from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    ordering = ['-publish']
    list_display = ('title', 'status', 'author', 'publish')
    list_filter = ('status', 'publish')
    prepopulated_fields = {'slug': ['title']}
    raw_id_fields = ('author',)
    search_fields = ('title', 'tease', 'body')

admin.site.register(Post, PostAdmin)
