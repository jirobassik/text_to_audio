from django.contrib import admin
from text_to_audio_manager.models import TaskAudioManagerModel


@admin.register(TaskAudioManagerModel)
class TaskAudioManagerAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'status', 'text', 'rel_user', 'time_add', 'is_deleted']
    list_filter = ['time_add']
