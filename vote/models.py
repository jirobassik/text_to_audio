import pathlib

from django.db import models

class VoteModel(models.Model):
    audio_name = models.CharField('Название голоса', max_length=20, null=False, blank=False, unique=True)
    audio_file = models.FileField('Путь к аудио')
    # TODO Можно добавить тэги к голосам стр 134
    # class Meta:
    #     ordering = ['audio_name']
    #     indexes = [
    #         models.Index(fields=['audio_name'])
    #     ]

    def __str__(self):
        return self.audio_name

    def delete(self, using=None, keep_parents=False):
        pathlib.Path('media', self.audio_file.name).unlink(missing_ok=False)
        # TODO добавить удаление сразу нескольких файлов
        super().delete()
