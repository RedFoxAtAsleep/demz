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




