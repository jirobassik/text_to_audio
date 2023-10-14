from django.contrib import admin
from history.models import HistoryModel


@admin.register(HistoryModel)
class AdminHistory(admin.ModelAdmin):
    list_display = ['text', 'audio_file', 'use_vote', 'time_add']
    list_filter = ['text', 'use_vote', 'time_add']
    search_fields = ['text', 'use_vote__audio_name']
    ordering = ['text', 'time_add']
