# -*- coding: utf-8 -*-
import os
import sys
import time

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from scripts.ucelery.celeries import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task
def f(x, loop):
    print('>>> {}'.format(x))
    for i in range(loop):
        pass
    print('<<< {}'.format(x))
    return x