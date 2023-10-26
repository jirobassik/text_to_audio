from django.shortcuts import render
from vote.models import VoteModel
from utils.server_converter.init_json_ser_req import text_converter_serializer, text_converter_request
from time import sleep

def text_to_audio(request):
    votes = VoteModel.objects.all()
    if 'converter' in request.POST:
        print('yes')
        text = request.POST.get('text', '')
        print(text)
        voice = request.POST.get('voice', 'emma')
        print(voice)
        preset = request.POST.get('preset', 'ultra_fast')
        print(preset)
        # sleep(180)
    # text = 'Hello my name Emma'
    # preset = 'fast'
    # audio_file = VoteModel.objects.get(id=3).audio_file
    # res = text_converter_serializer.encode(text=text, voice='emma', preset=preset)
    # print(res)
    # text_converter_request.get_request_data(res, audio_file.read())
    return render(request, 'text_converter/text_to_audio.html', {"votes": votes})
