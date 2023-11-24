import logging
import requests.exceptions as req_exc
import vanna.exceptions as van_exc
from utils.vanna_util.vanna_use import VannaUse


def vanna_get_queryset(query):
    def replace_percent(query_string: str) -> str:
        return query_string.replace('%', '%%')

    def add_id(query_string: str) -> str:
        split_str = query_string.split(" ")
        split_str.insert(1, 'id,')
        return " ".join(split_str)

    try:
        vanna_ = VannaUse()
        vanna_raw_query = replace_percent(add_id(vanna_.text_to_sql(query)))
        return vanna_raw_query
    except (van_exc.ConnectionError, van_exc.ValidationError, req_exc.ConnectionError) as e:
        logging.error(f'Vanna error {e}')
        return False
