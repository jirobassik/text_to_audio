from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import HistoryModel
from utils.vanna_util.vanna_run import vanna_get_queryset


class HistoryView(LoginRequiredMixin, ListView):
    model = HistoryModel
    context_object_name = 'history_entries'
    template_name = 'history/history.html'

    def get_queryset(self):
        return self.model.objects.history_user_access(self.request.user)


class HistoryDetailView(LoginRequiredMixin, DetailView):
    model = HistoryModel
    context_object_name = 'history_detail_entry'
    template_name = 'history/history_detail.html'

    def get_object(self, queryset=None):
        queryset = self.model.objects.history_user_access(self.request.user)
        return super().get_object(queryset)


def play_audio(request, audio_id):
    audio = get_object_or_404(HistoryModel, id=audio_id)
    audio_file = audio.audio_file.path

    with open(audio_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'inline; filename=' + audio.audio_file.name
        return response


class HistoryAiSearchView(LoginRequiredMixin, ListView):
    model = HistoryModel
    template_name = 'history/history_ai_search.html'
    context_object_name = 'history_ai_entries'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = True
        return context

    def get_queryset(self):
        query = self.request.GET.get('input_query', '')
        return vanna_get_queryset(self, query)


class HistorySearchView(LoginRequiredMixin, ListView):
    model = HistoryModel
    context_object_name = 'history_entries'
    template_name = 'history/history.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = True
        return context

    def get_queryset(self):
        query = self.request.GET.get('input_query', '')
        filter_query = self.model.objects.history_user_access(self.request.user).annotate(
            search=SearchVector('text', 'vote_mod__audio_name', 'user_vote_mod__audio_name')).filter(search=query)
        return filter_query
