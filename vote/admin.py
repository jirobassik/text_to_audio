from django.contrib import admin
from .models import VoteModel, AudioFileModel
from history.admin import HistoryModelInline


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

    @staticmethod
    def tag_list(obj):
        return u", ".join(o.name for o in obj.tags.all())

    # TODO добавить статистику по использованным голосам https://docs.djangoproject.com/en/4.1/ref/contrib/admin/


@admin.register(AudioFileModel)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'voice_name', 'audio_file']
