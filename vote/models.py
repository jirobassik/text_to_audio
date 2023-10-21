import pathlib

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class CommonVoteModel(models.Model):
    audio_name = models.CharField('Название голоса', max_length=20, null=False, blank=False, unique=True)
    tags = TaggableManager(verbose_name='Тэги', blank=False)

    class Meta:
        abstract = True
        ordering = ['audio_name']
        indexes = [
            models.Index(fields=['audio_name'])
        ]

    def __str__(self):
        return self.audio_name


class VoteModel(CommonVoteModel):
    audio_file = models.FileField('Путь к аудио', unique=True, upload_to='vote_media')

    def delete(self, using=None, keep_parents=False):
        pathlib.Path('media', self.audio_file.name).unlink(missing_ok=False)
        super().delete()

    def get_absolute_url(self):
        return reverse('vote-view')
