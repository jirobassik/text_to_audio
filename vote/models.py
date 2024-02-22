import pathlib

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.urls import reverse
from taggit.managers import TaggableManager
from history.models import HistoryModel
from utils.file_validation import extension_validation, content_validation, max_size_validation
from utils.redis_connect import r

class CommonVoteModel(models.Model):
    audio_name = models.CharField('Название голоса', max_length=20, null=False, blank=False, unique=True)
    tags = TaggableManager(verbose_name='Тэги', blank=False)
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False)

    class Meta:
        abstract = True
        ordering = ['audio_name']
        indexes = [
            models.Index(fields=['audio_name', 'is_deleted'])
        ]

    def __str__(self):
        return self.audio_name


class VoteModel(CommonVoteModel):
    his_models = GenericRelation(HistoryModel, related_query_name='vote_mod')

    def get_absolute_url(self):
        return reverse('vote-detail-view', args=[self.id])

@receiver(post_delete, sender=VoteModel)
def vote_post_delete(sender, instance, **kwargs):
    r.delete(f'voice:{instance.id}:object')

class AudioFileModel(models.Model):
    voice_name = models.ForeignKey(VoteModel, on_delete=models.CASCADE, verbose_name='Принадлежит голосу')
    audio_file = models.FileField('Путь к аудио', upload_to='vote_media',
                                  validators=[extension_validation, content_validation, max_size_validation])

    def __str__(self):
        return self.audio_file.name


@receiver(pre_delete, sender=AudioFileModel)
def audio_file_pre_delete(sender, instance, **kwargs):
    file_name = instance.audio_file.name
    path = pathlib.Path('media', file_name)
    if path.exists():
        path.unlink(missing_ok=False)
