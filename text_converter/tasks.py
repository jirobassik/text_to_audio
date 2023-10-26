from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from huey import crontab
from huey.contrib.djhuey import periodic_task, task, db_task
from history.models import HistoryModel
from vote.models import VoteModel
from time import sleep


@task()
def response_converter():
    sleep(10)
    response = 'Аудио файл'
    # new_view(response)
    new_view2(response)


# def new_view(voice):
#     return redirect('text-to-audio-voice', voice=voice)
#
#
# def new_view2(voice):
#     print('new_view2')
#     return HttpResponseRedirect(reverse('text-to-audio-voice', args=(voice,)))

@db_task()
def add_response_api_converter(text: str, voice: int, user):
    sleep(10)
    test_voice_file = VoteModel.objects.get(id=voice)
    HistoryModel(text=text, audio_file=test_voice_file.audio_file, use_vote=test_voice_file, user=user).save()
