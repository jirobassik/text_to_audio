from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector
from .models import HistoryModel
from utils.vanna_test import VannaUse
from operator import concat

vanna_ = VannaUse

class HistoryView(ListView):
    model = HistoryModel
    context_object_name = 'history_entries'
    template_name = 'history/history.html'


class HistoryAiSearchView(ListView):
    model = HistoryModel
    template_name = 'history/history_ai_search.html'
    context_object_name = 'history_ai_entries'

    def get_queryset(self):
        query = concat(self.request.GET.get('input_query', ''), ' in history_historymodel')  # TODO Может по другому?

        def add_id(query_string: str) -> str:
            split_str = query_string.split(" ")
            split_str.insert(1, 'id,')
            return " ".join(split_str)

        vanna_raw_query = add_id(vanna_.text_to_sql(query))
        query_set = self.model.objects.raw(vanna_raw_query)
        return query_set

class HistorySearchView(ListView):
    model = HistoryModel
    context_object_name = 'history_entries'
    template_name = 'history/history.html'

    def get_queryset(self):
        query = self.request.GET.get('input_query', '')
        filter_query = self.model.objects.annotate(
            search=SearchVector('text', 'use_vote__audio_name')).filter(search=query)
        return filter_query

