from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from taggit.models import Tag
from .models import VoteModel


class AudioView(ListView):
    model = VoteModel
    template_name = 'vote/audio.html'
    context_object_name = 'audio_files'


class TagAudioView(ListView):
    model = VoteModel
    template_name = 'vote/audio.html'
    context_object_name = 'audio_files'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        return self.model.objects.filter(tags__in=[tag])


class DetailAudioView(DetailView):
    model = VoteModel
    template_name = 'vote/vote_detail.html'
    context_object_name = 'audio_files_detail'

    def get_object(self, queryset=None):
        queryset = self.model.objects.prefetch_related('audiofilemodel_set')
        return super().get_object(queryset)
