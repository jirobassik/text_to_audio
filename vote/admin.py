import logging

from django.contrib import admin, messages
from requests.exceptions import SSLError, ConnectionError
from utils.server_converter.server_error import SendError
from .models import VoteModel, AudioFileModel
from history.admin import HistoryModelInline
from utils.server_converter.send import send_voice, del_voice
from utils.server_converter.init_json_ser_req import add_delete_voice_request_admin


class StackedInLineFileAdmin(admin.StackedInline):
    model = AudioFileModel


@admin.register(VoteModel)
class VoteAdmin(admin.ModelAdmin):
    inlines = [StackedInLineFileAdmin, HistoryModelInline]
    list_display = ['audio_name', 'tag_list']
    list_filter = ['audio_name']
    search_fields = ['audio_name']
    ordering = ['audio_name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def delete_model(self, request, obj):
        try:
            del_voice(obj.audio_name, add_delete_voice_request_admin)
            super().delete_model(request, obj)
        except (SSLError, ConnectionError, SendError) as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Что-то пошло не так, попробуйте позже')
            logging.error(e)

    def save_model(self, request, obj, form, change):
        try:
            send_voice(request.FILES.values(), obj.audio_name, add_delete_voice_request_admin)
            super().save_model(request, obj, form, change)
        except (SSLError, ConnectionError, SendError) as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, 'Что-то пошло не так, попробуйте позже')
            logging.error(e)

    @staticmethod
    def tag_list(obj):
        return u", ".join(o.name for o in obj.tags.all())

    # TODO добавить статистику по использованным голосам https://docs.djangoproject.com/en/4.1/ref/contrib/admin/


@admin.register(AudioFileModel)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'voice_name', 'audio_file']
