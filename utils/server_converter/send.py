from django.core.files.base import ContentFile

from history.models import HistoryModel
from utils.server_converter.init_json_ser_req import add_delete_voice_serializer, text_converter_serializer, \
    text_converter_request
from utils.convert_file_resp import convert_to_downloable
from utils.server_converter.server_error import SendError
from utils.redis_connect import r


def send_voice(files, audio_name, request_meth):
    data_json = add_delete_voice_serializer.encode(audio_name=audio_name)
    payload = {'data': (None, data_json, 'application/json')} | {
        audio_file.name: (audio_file.name, audio_file.read(), 'audio/wav') for audio_file in files}
    stat_code = request_meth.post_request_data(payload).status_code
    if not stat_code == 200:
        raise SendError(f'Send not working, status code {stat_code}')


def send_converter(text, voice_object, preset, optgroup_name):
    data_json = text_converter_serializer.encode(text=text, voice=voice_object, preset=preset, owner=optgroup_name)
    return text_converter_request.get_request(data_json)


def send_converter_register(text, voice_object, preset, optgroup_name, user, voice_id):
    response_converter = send_converter(text, voice_object, preset, optgroup_name)
    if response_converter.status_code == 200:
        byte_object_file = response_converter.content
        file = ContentFile(byte_object_file, 'gen_result.wav')
        HistoryModel(text=text, audio_file=file, content_object=voice_object, user=user).save()
        if optgroup_name == 'standart_v':
            r.incr(f'voice:{voice_id}:object')


def send_converter_anonym(text, voice_object, preset, optgroup_name):
    response = send_converter(text, voice_object, preset, optgroup_name)
    if not (stat_code := response.status_code) == 200:
        raise SendError(f'Converter not working, status code {stat_code}')
    return convert_to_downloable(response)


def del_voice(audio_name, request_meth):
    data_json = add_delete_voice_serializer.encode(audio_name=audio_name)
    stat_code = request_meth.delete_request_data(data_json).status_code
    if not stat_code == 200:
        raise SendError(f'Delete not working, status code {stat_code}')
