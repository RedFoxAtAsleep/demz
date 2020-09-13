# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import sys
import celery

app = celery.Celery(
    'some',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['ucelery.tasks']  # 注册的task的前缀
)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    # 方案一：命令行启动
    # celery -app path.to.module:celery_instance  worker
    # celery -A ucelery.celeries:app  worker -l info
    # 在其中注册的任务前缀是ucelery.tasks
    # ucelery.tasks.add
    # ucelery.tasks.mul
    # ucelery.tasks.xsum
    # 以上是任务注册的唯一标志

    # from ucelery.tasks import add, mul, xsum
    # 才能保证
    # ucelery.tasks.add
    # ucelery.tasks.mul
    # ucelery.tasks.xsum

    # 方案二：实例脚本启动
    # celery_instance.start(argv=['celery', 'worker', '-Q', 'celery', '-l', 'info', '-f', 'logs/message.log'])
    # 第一个参数是固定的，用于启动celery
    # 第二个参数是启动的celery组件，这里启动的是worker，用于执行任务
    # 第三个参数和第四个参数为一组，指定日志的级别
    # 第五个参数和第六个参数为一组，指定日志文件的位置

    import time
    from tasks import *
    app = celery.Celery(
        'some',
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0',
        include=['tasks']  # 注册的task的前缀
    )
    app.start(argv=['celery', 'worker', '-l', 'info'])  # 阻塞

    # runnning.py
    # from tasks import add, mul, xsum
    # r = add.delay(4, 4)
    # print(r.state, r.get())
    #
    # r = add.apply_async((4, 4), countdown=5)
    # for i in range(5):
    #     time.sleep(1)
    #     print(i+1, 's', r.state, r.get())
    #
    # r1 = app.AsyncResult(r.id)
    # r2 = app.AsyncResult('this-id-does-not-exits')
    # print(r.id, r.state)
    # print('this-id-does-not-exits', r.state)

    # 无论是方案一还是方案二
    # 保证注册的任务前缀和导入运行的任务的前缀保持一致












