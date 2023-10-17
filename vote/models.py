import pathlib

from django.db import models
from taggit.managers import TaggableManager


class VoteModel(models.Model):
    audio_name = models.CharField('Название голоса', max_length=20, null=False, blank=False, unique=True)
    audio_file = models.FileField('Путь к аудио', unique=True, upload_to='vote_media')
    tags = TaggableManager(verbose_name='Тэги', blank=False)

    class Meta:
        ordering = ['audio_name']
        indexes = [
            models.Index(fields=['audio_name'])
        ]

    def delete(self, using=None, keep_parents=False):
        pathlib.Path('media', self.audio_file.name).unlink(missing_ok=False)
        super().delete()

    def __str__(self):
        return self.audio_name
