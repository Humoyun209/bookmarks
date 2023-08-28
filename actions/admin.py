from actions.models import Action

from django.contrib import admin


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'verb', 'target', 'created']
    list_filter = ['created', 'user']
    search_fields = ['verb', 'user']