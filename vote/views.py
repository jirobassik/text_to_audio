from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView

from .models import VoteModel


def play_audio(request, audio_id):
    audio = get_object_or_404(VoteModel, id=audio_id)
    audio_file = audio.audio_file.path

    with open(audio_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename=' + audio.audio_file.name
        return response


def audio_list(request):
    audio_files = VoteModel.objects.all()
    return render(request, 'vote/audio.html', {'audio_files': audio_files})


class AudioView(ListView):
    model = VoteModel
    template_name = 'vote/audio.html'
    context_object_name = 'audio_files'
