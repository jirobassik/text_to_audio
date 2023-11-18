import logging

from django import template

from utils.redis_connect import r
from redis.exceptions import ConnectionError
register = template.Library()


@register.simple_tag
def get_total_usage(voice_id: int):
    try:
        total_usage = r.get(f'voice:{voice_id}:object')
        return int(total_usage) if total_usage else 0
    except ConnectionError as e:
        logging.error(e)
        return 'Нет данных'
