import pathlib

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from history.models import HistoryModel


@admin.register(HistoryModel)
class AdminHistory(admin.ModelAdmin):
    list_display = ['text', 'audio_file', 'use_vote', 'time_add', 'user_history_link']
    list_filter = ['text', 'use_vote', 'time_add', 'user']
    search_fields = ['text', 'use_vote__audio_name', 'user']
    ordering = ['text', 'time_add']

    def delete_queryset(self, request, queryset):
        paths = queryset.values_list('audio_file', flat=True)
        for file_path in paths:
            pathlib.Path('media', file_path).unlink(missing_ok=False)
        super().delete_queryset(request, queryset)

    def user_history_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_history_link.short_description = 'Владелец'
