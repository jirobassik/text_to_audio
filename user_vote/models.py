import pathlib

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from vote.models import CommonVoteModel


class UserAccessManager(models.Manager):
    def access_user(self, user):
        return super().get_queryset().filter(user_vote=user)


# class UserVoteModel(CommonVoteModel):
#     user_audio_file = models.FileField('Путь к аудио', unique=True, upload_to='user_vote_media')
#     user_vote = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     objects = UserAccessManager()
#
#     def delete(self, using=None, keep_parents=False):
#         pathlib.Path('media', self.user_audio_file.name).unlink(missing_ok=False)
#         super().delete()
#
#     def get_absolute_url(self):
#         return reverse('vote-detail-user', args=[self.id])


class UserVoteModel(CommonVoteModel):
    user_vote = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = UserAccessManager()

    def get_absolute_url(self):
        return reverse('vote-detail-user', args=[self.id])


class UserAudioFile(models.Model):
    user_voice_name = models.ForeignKey(UserVoteModel, on_delete=models.CASCADE, verbose_name='Принадлежит голосу')
    audio_file = models.FileField('Путь к аудио', upload_to='user_vote_media')

    def delete(self, using=None, keep_parents=False):
        pathlib.Path('media', self.audio_file.name).unlink(missing_ok=False)
        super().delete()

    def __str__(self):
        return self.audio_file.name
