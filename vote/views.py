from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from taggit.models import Tag
from .models import VoteModel


def play_audio(request, audio_id):
    audio = get_object_or_404(VoteModel, id=audio_id)
    audio_file = audio.audio_file.path

    with open(audio_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename=' + audio.audio_file.name
        return response


# TODO можно добавить часто используемые голоса
class AudioView(ListView):
    model = VoteModel
    template_name = 'vote/audio.html'
    context_object_name = 'audio_files'


class TagAudioView(ListView):
    template_name = 'vote/audio.html'
    context_object_name = 'audio_files'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        return VoteModel.objects.filter(tags__in=[tag])
