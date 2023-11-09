from django.contrib import messages
from vanna.exceptions import ConnectionError, ValidationError

from utils.vanna_util.vanna_use import VannaUse


def vanna_get_queryset(self, query):
    def add_id(query_string: str) -> str:
        split_str = query_string.split(" ")
        split_str.insert(1, 'id,')
        return " ".join(split_str)

    try:
        vanna_ = VannaUse()
        vanna_raw_query = add_id(vanna_.text_to_sql(query))
        query_set = self.model.objects.history_user_access(self.request.user).raw(vanna_raw_query)
        return query_set
    except (ConnectionError, ValidationError):
        self.template_name = 'history/history.html'
        self.context_object_name = 'history_entries'
        query_set = self.model.objects.history_user_access(self.request.user)
        messages.error(self.request, 'Интеллектуальный поиск не работает, попробуйте '
                                     'вести другой запрос или свяжитесь с администратором')
        return query_set
