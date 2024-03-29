from huey.contrib.djhuey import db_task
from user_vote.models import UserVoteModel
from vote.models import VoteModel
from utils.server_converter.send import send_converter_register
from utils.audio_to_text import check_text_type


@db_task(priority=50)
def add_response_api_converter(text: str, voice_id: int, preset: str, owner: str, pk, user):
    text = check_text_type(text, pk)
    voice_object = VoteModel.objects.get(id=voice_id) if owner == 'standart_v' \
        else UserVoteModel.objects.get(id=voice_id)
    send_converter_register(text, voice_object, preset, owner, user, voice_id)
