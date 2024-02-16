from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.views.generic import ListView, DetailView
from redis.exceptions import ConnectionError
from taggit.models import Tag
from .models import VoteModel


class AudioView(ListView):
    model = VoteModel
    template_name = 'vote/audio.html'
    context_object_name = 'audio_files'

    def get_queryset(self):
        try:
            subjects = cache.get('all_vote')
            if not subjects:
                subjects = self.model.objects.all()
                cache.set('all_vote', subjects, 30)
            return subjects
        except ConnectionError:
            subjects = self.model.objects.all()
            return subjects


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
