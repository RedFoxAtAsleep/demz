# -*- coding: utf-8 -*-
import time

from celery import shared_task


@shared_task
def fff(name, n):
    print(">>> {}".format(name))
    time.sleep(n)
    print("{} <<<".format(name))
