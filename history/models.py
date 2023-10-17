import pathlib

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from vote.models import VoteModel


class HistoryModel(models.Model):
    text = models.CharField('Озвученный текст', max_length=100, null=False, blank=False)
    audio_file = models.FileField('Результат озвучивания',
                                  upload_to='history_media', unique=True)  # TODO Подумать про хранение файлов
    use_vote = models.ForeignKey(VoteModel, on_delete=models.CASCADE, verbose_name='Используемый голос')
    time_add = models.DateTimeField('Время добавления', auto_created=True, editable=False,
                                    auto_now_add=True)

    # TODO Можно добавить менеджеры? стр 68
    class Meta:
        ordering = ['text']
        indexes = [
            models.Index(fields=['text'])
        ]

    def delete(self, using=None, keep_parents=False):
        pathlib.Path('media', self.audio_file.name).unlink(missing_ok=False)
        super().delete()

    def __str__(self):
        return self.text


# TODO Разобраться с сигналами
@receiver(pre_delete, sender=HistoryModel)
def history_pre_delete(sender, instance, **kwargs):
    file_name = instance.audio_file.name
    pathlib.Path('media', file_name).unlink(missing_ok=False)
