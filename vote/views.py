from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from taggit.models import Tag
from .models import VoteModel
from django.contrib.auth.mixins import LoginRequiredMixin

# TODO можно добавить часто используемые голоса
class AudioView(LoginRequiredMixin, ListView):
    model = VoteModel
    template_name = 'vote/audio.html'
    context_object_name = 'audio_files'


class TagAudioView(LoginRequiredMixin, ListView):
    template_name = 'vote/audio.html'
    context_object_name = 'audio_files'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        return VoteModel.objects.filter(tags__in=[tag])
