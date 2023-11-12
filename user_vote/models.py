import pathlib

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from utils.file_validation import content_validation, extension_validation, max_size_validation
from history.models import HistoryModel
from vote.models import CommonVoteModel


class UserAccessManager(models.Manager):
    def access_user(self, user):
        return super().get_queryset().filter(user_vote=user)


class UserVoteModel(CommonVoteModel):  # TODO Если нет связанных файлов, то нельзя что-то
    user_vote = models.ForeignKey(User, on_delete=models.CASCADE)
    his_models = GenericRelation(HistoryModel, related_query_name='user_vote_mod')

    objects = UserAccessManager()

    def get_absolute_url(self):
        return reverse('vote-detail-user', args=[self.id])


class UserAudioFile(models.Model):
    user_voice_name = models.ForeignKey(UserVoteModel, on_delete=models.CASCADE, verbose_name='Принадлежит голосу')
    audio_file = models.FileField('Путь к аудио', upload_to='user_vote_media',
                                  validators=[extension_validation, content_validation, max_size_validation])

    def __str__(self):
        return self.audio_file.name


@receiver(pre_delete, sender=UserAudioFile)
def user_audio_file_pre_delete(sender, instance, **kwargs):
    file = instance.audio_file.name
    pathlib.Path('media', file).unlink(missing_ok=False)
