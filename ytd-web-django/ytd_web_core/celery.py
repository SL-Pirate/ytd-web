from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from ytd_web import redis
from ytd_web_core.util import clean_immediate
from time import sleep
from ytd_web_core import keep_time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ytd_web.settings')

app = Celery('ytd_web_core', broker="redis://localhost:6379", backend="redis://localhost:6379")

app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def clean_func(item: str, id: int) -> None:
    sleep(keep_time * 60)
    clean_immediate(item)

    from ytd_web_core.models import Downloadable
    downloadable: Downloadable = Downloadable.objects.get(id=id)
    downloadable.delete()
