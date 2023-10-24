from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import HistoryModel
from utils.vanna_util.vanna_run import vanna_get_queryset
from operator import concat


class HistoryView(LoginRequiredMixin, ListView):
    model = HistoryModel
    context_object_name = 'history_entries'
    template_name = 'history/history.html'


class HistoryAiSearchView(LoginRequiredMixin, ListView):
    model = HistoryModel
    template_name = 'history/history_ai_search.html'
    context_object_name = 'history_ai_entries'

    def get_queryset(self):
        query = concat(self.request.GET.get('input_query', ''), ' in history_historymodel')  # TODO Может по другому?
        return vanna_get_queryset(self, query)


class HistorySearchView(LoginRequiredMixin, ListView):
    model = HistoryModel
    context_object_name = 'history_entries'
    template_name = 'history/history.html'

    def get_queryset(self):
        query = self.request.GET.get('input_query', '')
        filter_query = self.model.objects.annotate(
            search=SearchVector('text', 'use_vote__audio_name')).filter(search=query)
        return filter_query
