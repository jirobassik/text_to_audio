from datetime import datetime, timedelta

from huey import crontab
from huey.contrib.djhuey import db_task, periodic_task
from huey.contrib.djhuey import signal

from text_to_audio_manager.models import TaskAudioManagerModel
from utils.static_data import status_choice


@db_task()
def delete_audio_manager():
    TaskAudioManagerModel.objects.filter(time_add__lte=datetime.now() - timedelta(hours=1)).update(is_deleted=True)


@periodic_task(crontab(minute='*/1'))
def delete_audio_time():
    delete_audio_manager()


@db_task()
def add_manager(task_id: str, text: str, status: str, user):
    filter_task_id = TaskAudioManagerModel.objects.filter(task_id=task_id)
    if filter_task_id.exists():
        filter_task_id.update(status=status)
    else:
        TaskAudioManagerModel.objects.create(task_id=task_id, text=text, status=status, rel_user=user)


@signal()
def audio_signal(signal, task, exc=None):
    if task.name == 'add_response_api_converter':
        task_text, task_user = task.args[0], task.args[-1]
        add_manager(task.id, task_text, status_choice.get(signal, 'Нет данных'), task_user)
