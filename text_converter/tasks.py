from django.core.files.base import ContentFile
from huey.contrib.djhuey import db_task
from history.models import HistoryModel
from user_vote.models import UserVoteModel
from utils.server_converter.init_json_ser_req import text_converter_serializer, add_delete_voice_request
from vote.models import VoteModel


@db_task()
def add_response_api_converter(text: str, voice_id: int, preset: str, owner: str, user):
    voice_object = VoteModel.objects.get(id=voice_id) if owner == 'standart_v' \
        else UserVoteModel.objects.get(id=voice_id)
    data_json = text_converter_serializer.encode(text=text, voice=voice_object, preset=preset, owner=owner)
    response_converter = add_delete_voice_request.get_request(data_json)
    if response_converter.status_code == 200:
        byte_object_file = response_converter.content
        file = ContentFile(byte_object_file, 'gen_result.wav')
        HistoryModel(text=text, audio_file=file, content_object=voice_object, user=user).save()
