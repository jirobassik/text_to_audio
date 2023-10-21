import pathlib

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from vote.models import CommonVoteModel


class UserVoteModel(CommonVoteModel):
    user_audio_file = models.FileField('Путь к аудио', unique=True, upload_to='user_vote_media')
    user_vote = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, using=None, keep_parents=False):
        pathlib.Path('media', self.user_audio_file.name).unlink(missing_ok=False)
        super().delete()

    def get_absolute_url(self):
        return reverse('vote-view-user')
