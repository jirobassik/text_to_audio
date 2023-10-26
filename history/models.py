import pathlib

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
from vote.models import VoteModel

class HistoryUserManager(models.Manager):
    def history_user_access(self, user):
        return super().get_queryset().filter(user=user)

class HistoryModel(models.Model):
    text = models.CharField('Озвученный текст', max_length=100, null=False, blank=False)
    audio_file = models.FileField('Результат озвучивания',
                                  upload_to='history_media', unique=False)  # TODO Подумать про хранение файлов
    use_vote = models.ForeignKey(VoteModel, on_delete=models.CASCADE, verbose_name='Используемый голос')
    time_add = models.DateTimeField('Время добавления', auto_created=True, editable=False,
                                    auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    objects = HistoryUserManager()

    class Meta:
        ordering = ['text']
        indexes = [
            models.Index(fields=['text'])
        ]

    def delete(self, using=None, keep_parents=False):
        pathlib.Path('media', self.audio_file.name).unlink(missing_ok=False)
        super().delete()

    def get_absolute_url(self):
        return reverse('history-detail', args=[self.id])

    def __str__(self):
        return self.text


# TODO Разобраться с сигналами
@receiver(pre_delete, sender=HistoryModel)
def history_pre_delete(sender, instance, **kwargs):
    file_name = instance.audio_file.name
    pathlib.Path('media', file_name).unlink(missing_ok=False)
