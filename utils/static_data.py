from types import MappingProxyType

status_choice = MappingProxyType({
    'executing': 'Выполняется',
    'complete': 'Завершен',
    'error': 'Ошибка',
    'locked': 'Ошибка',
    'revoked': 'Ошибка',
    'interrupted': 'Ошибка',
    'expired': 'Срок истек',
    'retrying': 'Повторное выполнение',
    'scheduled': 'Добавлено в расписание',
})
