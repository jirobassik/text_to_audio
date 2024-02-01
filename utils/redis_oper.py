from utils.redis_connect import r
from redis.exceptions import ConnectionError

def get_executing_count(user):
    try:
        return r.scard(f'executing-tasks:user:{user}')
    except ConnectionError:
        return True


def change_status(status, task_user, task):
    if status == 'executing':
        r.sadd(f'executing-tasks:user:{task_user}', task.id)
    else:
        r.srem(f'executing-tasks:user:{task_user}', task.id)
