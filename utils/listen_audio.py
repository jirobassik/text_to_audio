from django.http import HttpResponse
from django.shortcuts import get_object_or_404


class ListenAudio:
    __slots__ = ('model', 'audio_file')

    def __init__(self, model, audio_file):
        self.model = model
        self.audio_file = audio_file

    def play_audio(self, request, audio_id):
        audio = get_object_or_404(self.model, id=audio_id)
        audio_file = audio.audio_file.path

        with open(audio_file, 'rb') as file:
            response = HttpResponse(file.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'inline; filename=' + audio.audio_file.name
            return response
