import pathlib

from django.contrib import admin
from history.models import HistoryModel


@admin.register(HistoryModel)
class AdminHistory(admin.ModelAdmin):
    list_display = ['text', 'audio_file', 'use_vote', 'time_add']
    list_filter = ['text', 'use_vote', 'time_add']
    search_fields = ['text', 'use_vote__audio_name']
    ordering = ['text', 'time_add']

    def delete_queryset(self, request, queryset):
        paths = queryset.values_list('audio_file', flat=True)
        for file_path in paths:
            pathlib.Path('media', file_path).unlink(missing_ok=False)
        super().delete_queryset(request, queryset)
