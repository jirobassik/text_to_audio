from django.contrib import admin
from .models import VoteModel


@admin.register(VoteModel)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['audio_name', 'audio_file']
    list_filter = ['audio_name']
    search_fields = ['audio_name']
    ordering = ['audio_name']
    # TODO добавить статистику по использованным голосам https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
