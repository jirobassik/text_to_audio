import pathlib

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from taggit.managers import TaggableManager
from history.models import HistoryModel
from utils.file_validation import extension_validation, content_validation, max_size_validation
from utils.server_converter.init_json_ser_req import add_delete_voice_request_admin, add_delete_voice_serializer

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
    his_models = GenericRelation(HistoryModel, related_query_name='vote_mod')

    def get_absolute_url(self):
        return reverse('vote-detail-view', args=[self.id])

@receiver(pre_delete, sender=VoteModel)
def audio_pre_delete(sender, instance, **kwargs):
    data_json = add_delete_voice_serializer.encode(audio_name=instance.audio_name, creator='user')
    add_delete_voice_request_admin.delete_request_data(data_json)

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

@receiver(pre_save, sender=AudioFileModel)
def audio_file_pre_save(sender, instance, **kwargs):
    audio_name, audio_file = VoteModel.objects.get(id=instance.voice_name_id).audio_name, instance.audio_file
    data_json = add_delete_voice_serializer.encode(audio_name=audio_name, creator='user')
    payload = {'data': (None, data_json, 'application/json')} | {
        audio_file.name: (audio_file.name, audio_file.read(), 'audio/wav')}
    add_delete_voice_request_admin.post_request_data(payload)
