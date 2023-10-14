from django.db import models
from vote.models import VoteModel


class HistoryModel(models.Model):
    text = models.CharField('Озвученный текст', max_length=100, null=False, blank=False)
    audio_file = models.FileField('Результат озвучивания',
                                  upload_to='history/history_media')  # TODO Подумать про хранение файлов
    use_vote = models.ForeignKey(VoteModel, on_delete=models.CASCADE, verbose_name='Используемый голос')
    time_add = models.DateTimeField('Время добавления', auto_created=True, editable=False, auto_now_add=True) # TODO Сделать нормальное время
    # TODO Можно добавить менеджеры? стр 68
    # class Meta:
    #     ordering = ['text']
    #     indexes = [
    #         models.Index(fields=['text'])
    #     ]

    def __str__(self):
        return self.text
