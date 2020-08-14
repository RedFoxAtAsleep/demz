# -*- coding: utf-8 -*-


from datetime import datetime
import time
import os
import logging
from django.urls import path, include
from apscheduler.schedulers.background import BackgroundScheduler
from . import views


urlpatterns = [
    path('', views.index),
    path('download', views.download),
]

logging.basicConfig(level=logging.ERROR)


def tick():
    print('tick ... ... ...')


scheduler = BackgroundScheduler()
scheduler.add_job(tick, 'interval', seconds=1)
# FATAL CRITICAL ERROR WARNING NFO DEBUG
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARN)
logging.getLogger('apscheduler.scheduler').setLevel(logging.WARN)
scheduler.start()


