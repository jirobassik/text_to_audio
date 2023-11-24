import logging
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import ProgrammingError
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
        key = (str(self.request.user.id) + query).replace(' ', '')
        if sql_val := self.request.session.get(key, False):
            return self.model.objects.history_user_access(self.request.user).raw(sql_val)
        else:
            if (vanna_sql := vanna_get_queryset(query)) and (query_set := self.try_raw_queryset(vanna_sql)):
                self.request.session[key] = vanna_sql
                return query_set
            else:
                return self.error_view()

    def try_raw_queryset(self, raw_query):
        try:
            query_set = self.model.objects.history_user_access(self.request.user).raw(raw_query)
            if query_set:
                pass
            return query_set
        except (IndexError, ProgrammingError) as e:
            logging.error(f'Check queryset error {e}')
            return False

    def error_view(self):
        self.template_name = 'history/history.html'
        self.context_object_name = 'history_entries'
        query_set = self.model.objects.history_user_access(self.request.user)
        messages.error(self.request, 'Интеллектуальный поиск не работает, попробуйте '
                                     'вести другой запрос или свяжитесь с администратором')
        return query_set


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
