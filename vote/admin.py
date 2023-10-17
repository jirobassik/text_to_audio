import pathlib

from django.contrib import admin
from .models import VoteModel


@admin.register(VoteModel)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['audio_name', 'audio_file', 'tag_list']
    list_filter = ['audio_name']
    search_fields = ['audio_name']
    ordering = ['audio_name']

    def delete_queryset(self, request, queryset):
        paths = queryset.values_list('audio_file', flat=True)
        for file_path in paths:
            pathlib.Path('media', file_path).unlink(missing_ok=False)
        super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    @staticmethod
    def tag_list(obj):
        return u", ".join(o.name for o in obj.tags.all())

    # TODO добавить статистику по использованным голосам https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
