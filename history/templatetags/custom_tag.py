from types import MappingProxyType
from django import template

register = template.Library()


@register.simple_tag
def get_columns_name(column_name: str):
    dict_func = MappingProxyType({'text': f'Озвученный текст ({column_name})',
                                  'audio_file': f'Результат озвучивания ({column_name})',
                                  'use_vote': f'Используемый голос ({column_name})',
                                  'time_add': f'Время добавления ({column_name})', })
    return dict_func.get(column_name, 'Не найдено (not found)')

@register.simple_tag
def get_column_data(column_name: str, ai_entry):
    dict_func = MappingProxyType({'text': ai_entry.text,
                                  'audio_file': ai_entry.audio_file,
                                  'use_vote': ai_entry.use_vote,
                                  'time_add': ai_entry.time_add, })
    return dict_func.get(column_name, 'Не найдено (not found)')

@register.simple_tag
def get_columns(raw_query_set):
    return [column for column in raw_query_set.columns if column != 'id']
