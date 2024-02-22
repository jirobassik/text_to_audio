import pathlib

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User


class HistoryUserManager(models.Manager):
    def history_user_access(self, user):
        return super().get_queryset().filter(user=user)


class HistoryModel(models.Model):
    text = models.CharField('Озвученный текст', max_length=400, null=False, blank=False)
    audio_file = models.FileField('Результат озвучивания',
                                  upload_to='history_media', unique=False)  # TODO Подумать про хранение файлов
    time_add = models.DateTimeField('Время добавления', auto_created=True, editable=False,
                                    auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=Q(model__in=['uservotemodel', 'votemodel']),
                                     verbose_name='Тип голоса')
    object_id = models.PositiveIntegerField(verbose_name='Принадлежит голосу')
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_deleted = models.BooleanField(verbose_name='Удалено', default=False)

    objects = HistoryUserManager()

    class Meta:
        ordering = ["-time_add", "text"]
        indexes = [
            models.Index(fields=["text", "content_type", "object_id", "time_add"])
        ]

    def get_absolute_url(self):
        return reverse('history-detail', args=[self.id])

    def get_absolute_delete_url(self):
        return reverse('history-delete', args=[self.id])

    def __str__(self):
        return self.text


@receiver(pre_delete, sender=HistoryModel)
def history_pre_delete(sender, instance, **kwargs):
    file_name = instance.audio_file.name
    path = pathlib.Path('media', file_name)
    if path.exists():
        path.unlink(missing_ok=False)
