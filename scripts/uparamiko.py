# -*- coding: utf-8 -*-
import paramiko
import logging
import time
from paramiko.transport import Transport
import asyncio
import apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler




logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('paramiko.transport').setLevel(logging.ERROR)

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


if __name__ == '__main__':
    host = '120.78.123.249'
    user = 'root'
    password = 'Ali@123456'
    from_ = '/Users/zhaojinhui/github/demz/material/imgurls'
    to_ = '/root/imgurls'
    timeout = 15
    sftp_push_file(host, user, password, from_, to_)

    from_ = '/root/imgurls'
    to_ = '/Users/zhaojinhui/github/demz/material/{}imgurls'.format(time.asctime())

    async def parallel():
        await asyncio.gather(*[sftp_pull_file(host, user, password, from_, to_) for i in range(3)])
    asyncio.run(parallel())
    logging.info('end')





