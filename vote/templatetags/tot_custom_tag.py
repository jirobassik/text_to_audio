from django import template

from utils.redis_connect import r

register = template.Library()


@register.simple_tag
def get_total_usage(voice_id: int):
    total_usage = r.get(f'voice:{voice_id}:object')
    return int(total_usage) if total_usage else 0
