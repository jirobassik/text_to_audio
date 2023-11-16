from utils.server_converter.init_json_ser_req import add_delete_voice_serializer
from utils.server_converter.server_error import SendError


def send_voice(files, audio_name, request_meth):
    data_json = add_delete_voice_serializer.encode(audio_name=audio_name)
    payload = {'data': (None, data_json, 'application/json')} | {
        audio_file.name: (audio_file.name, audio_file.read(), 'audio/wav') for audio_file in files}
    stat_code = request_meth.post_request_data(payload).status_code
    if not stat_code == 200:
        raise SendError(f'Send not working, status code {stat_code}')


def del_voice(audio_name, request_meth):
    data_json = add_delete_voice_serializer.encode(audio_name=audio_name)
    stat_code = request_meth.delete_request_data(data_json).status_code
    if not stat_code == 200:
        raise SendError(f'Delete not working, status code {stat_code}')
