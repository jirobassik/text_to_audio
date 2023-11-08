from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from huey import crontab
from huey.contrib.djhuey import periodic_task, task, db_task
from history.models import HistoryModel
from user_vote.models import UserVoteModel
from utils.server_converter.init_json_ser_req import text_converter_serializer
from vote.models import VoteModel
from time import sleep


# @task()
# def response_converter():
#     sleep(10)
#     response = 'Аудио файл'
#     # new_view(response)
#     new_view2(response)


# def new_view(voice):
#     return redirect('text-to-audio-voice', voice=voice)
#
#
# def new_view2(voice):
#     print('new_view2')
#     return HttpResponseRedirect(reverse('text-to-audio-voice', args=(voice,)))

@db_task()
def add_response_api_converter(text: str, voice_id: int, preset: str, owner: str, user):
    voice_object = VoteModel.objects.get(id=voice_id).audio_name if owner == 'standart_v' \
        else UserVoteModel.objects.get(id=voice_id).audio_name
    data_json = text_converter_serializer.encode(text=text, voice=voice_object.audio_name, preset=preset, owner=owner)
    sleep(10)
    # HistoryModel(text=text, audio_file=test_voice_file.audio_file, use_vote=voice_object, user=user).save()
