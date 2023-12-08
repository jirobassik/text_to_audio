from huey import crontab
from huey.contrib.djhuey import periodic_task

from django.core.management import call_command


@periodic_task(crontab(hour="*/2"), priority=30)
def clear_expired_sessions():
    return call_command("clearsessions")
