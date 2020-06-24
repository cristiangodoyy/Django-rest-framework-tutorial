from django.contrib import admin
from snippets.models import Snippet, Comment, Project, Error


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'created', 'title', 'code', 'project')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('supervisor', 'description', 'snippet')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ('type', )
