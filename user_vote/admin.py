import pathlib

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from user_vote.models import UserVoteModel, UserAudioFile


@admin.register(UserVoteModel)
class UserVoteAdmin(admin.ModelAdmin):
    list_display = ['audio_name', 'user_vote_link', 'tag_list']
    list_filter = ['audio_name', 'user_vote']
    search_fields = ['audio_name', 'user_vote']
    ordering = ['audio_name', 'user_vote']

    # def delete_queryset(self, request, queryset):
    #     user_paths = queryset.values_list('user_audio_file', flat=True)
    #     for path in user_paths:
    #         pathlib.Path('media', path).unlink(missing_ok=False)
    #     super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def user_vote_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user_vote.id])
        return format_html('<a href="{}">{}</a>', url, obj.user_vote.username)

    user_vote_link.short_description = 'Владелец'
    tag_list.short_description = 'Тэги'


@admin.register(UserAudioFile)
class UserAudioFileAdmin(admin.ModelAdmin): # TODO Добавить удаление через админку
    list_display = ['id', 'audio_file', 'user_voice_name']
