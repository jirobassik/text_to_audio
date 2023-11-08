from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline
from history.models import HistoryModel


class HistoryModelInline(GenericTabularInline):
    model = HistoryModel

@admin.register(HistoryModel)
class AdminHistory(admin.ModelAdmin):
    list_display = ['text', 'audio_file', 'time_add', 'user_history_link']
    list_filter = ['text', 'time_add', 'user']
    search_fields = ['text' 'user']
    ordering = ['text', 'time_add']

    def user_history_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_history_link.short_description = 'Владелец'
