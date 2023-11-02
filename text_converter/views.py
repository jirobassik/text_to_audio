from django.shortcuts import render
from vote.models import VoteModel
from user_vote.models import UserVoteModel
from utils.server_converter.init_json_ser_req import text_converter_serializer, text_converter_request
from text_converter.tasks import add_response_api_converter
def text_to_audio(request, voice=None):
    votes = VoteModel.objects.values()
    # print(votes)
    # print('----------------')
    # user_votes = UserVoteModel.objects.values('id', 'audio_name', 'user_audio_file')
    # print(user_votes)
    # print('-----------------')
    # all_votes = votes.union(user_votes, all=True)
    # print(all_votes)

    if 'converter' in request.POST:
        text = request.POST.get('text', '')
        voice = request.POST.get('voice', 'emma')
        preset = request.POST.get('preset', 'ultra_fast')
        data_json = text_converter_serializer.encode(text=text, voice=voice, preset=preset)
        audio_file = VoteModel.objects.get(id=voice).audio_file
        payload = {
            'data': (None, data_json, 'application/json'),
            'file1': (audio_file.name, audio_file.read(), 'audio/mp3'),
            'file2': (audio_file.name, audio_file.read(), 'audio/mp3')
        }

        text_converter_request.get_request_data(payload)
        # add_response_api_converter(text, voice, request.user)

    # text = 'Hello my name Emma'
    # preset = 'fast'
    # audio_file = VoteModel.objects.get(id=3).audio_file
    # res = text_converter_serializer.encode(text=text, voice='emma', preset=preset)
    # print(res)

    context = {"votes": votes, "voice": voice}
    # print(context)
    return render(request, 'text_converter/text_to_audio.html', context)
