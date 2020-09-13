from django.test import TestCase

# Create your tests here.

import asyncio
import threading
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BaseScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
import logging
import time
import paramiko
from paramiko.transport import Transport


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logging.getLogger('apscheduler.executors.default').setLevel(logging.WARN)
logging.getLogger('apscheduler.scheduler').setLevel(logging.WARN)

def my_schedule_job():
    print("Callback runs in thread %s" % (threading.current_thread(),))


async def my_coroutine():
    logger.info(111)
    print(111)
    await asyncio.sleep(2)
    # print("Coroutine runs in %s" % (threading.current_thread(),))
    logger.info(222)
    print(222)
    await asyncio.sleep(2)
    logger.info(333)
    print(333)

    await asyncio.sleep(10)


def asyncf(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, func, *args, **kwargs)
    return wrapper

@asyncf
def sftp_push_file(host, user, password, to_, from_):
    """
    上传文件，注意：不支持文件夹
    :param host: 主机名
    :param user: 用户名
    :param password: 密码
    :param from_: 远程路径，比如：/home/sdn/tmp.txt
    :param to_: 本地路径，比如：D:/text.txt
    :param timeout: 超时时间(默认)，必须是int类型
    :return: bool
    """
    logging.debug('SSH FILE PUSH')
    try:
        t = Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(to_, from_)
        t.close()
        logging.info('SSH FILE PUSH SUCCESS')
        return True
    except Exception as e:
        logging.error(str(type(e)) + ' ' + e.strerror)
        logging.error('SSH FILE PUSH FAIL')
        return False

@asyncf
def sftp_pull_file(host, user, password, to_, from_):
    """
    上传文件，注意：不支持文件夹
    :param host: 主机名
    :param user: 用户名
    :param password: 密码
    :param from_: 远程路径，比如：/home/sdn/tmp.txt
    :param to_: 本地路径，比如：D:/text.txt
    :param timeout: 超时时间(默认)，必须是int类型
    :return: bool
    """
    logging.debug('SSH FILE PULL')
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(to_, from_)
        t.close()
        logging.info('SSH FILE PULL SUCCESS')
        return True
    except Exception as e:
        logging.error(str(type(e)) + ' ' + e.strerror)
        logging.error('SSH FILE PULL FAIL')
        return False

def scanner():
    logger.debug('scanning...')


if __name__ == '__main__':
    host = '120.78.123.249'
    user = 'root'
    password = 'Ali@123456'
    from_ = '/Users/zhaojinhui/github/demz/material/imgurls'
    to_ = '/root/imgurls'
    timeout = 15


    sftp_pull_file(host, user, password, from_.format(time.time_ns()), to_)
    print("Main runs in %s" % (threading.current_thread(),))
    loop = asyncio.new_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_job(
        sftp_push_file,
        'interval', seconds=10,
        args=(host, user, password, from_.format(time.time_ns()), to_)
    )
    scheduler.start()