# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

# Celery Client
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demz.settings')  # 在最前
app = Celery(
    'demz',
    broker='redis://localhost:6379/0'
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update({})
app.conf.beat_schedule = {
    'fff-every-5-seconds': {
        'task': 'someapp.tasks.fff',
        'schedule': 5.0,
        'args': ('x', 10)
    },
}
app.autodiscover_tasks()


if __name__ == '__main__':
    app.start()
