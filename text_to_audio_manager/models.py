from django.contrib.auth.models import User
from django.db import models


class TaskAudioManagerModel(models.Model):
    task_id = models.CharField(verbose_name='ID задачи', max_length=100, unique=True)
    rel_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель задачи')
    status = models.CharField(verbose_name='Статус задачи', max_length=100,
                              null=False, blank=False)
    text = models.CharField('Текст', max_length=400, null=False, blank=False)
    time_add = models.DateTimeField('Время добавления задачи', auto_created=True, editable=False,
                                    auto_now_add=True)
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False)

    class Meta:
        ordering = ['time_add']
        indexes = [
            models.Index(fields=('task_id', 'time_add'))
        ]

    def __str__(self):
        return self.task_id
