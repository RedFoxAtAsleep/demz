# -*- coding: utf-8 -*-
import paramiko
import logging
import os
import time
from paramiko.transport import Transport
import asyncio


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('paramiko.transport').setLevel(logging.WARNING)


def ssh_exec_command(host, user, password, cmd):
    """
    使用ssh连接远程服务器执行命令
    :param host: 主机名
    :param user: 用户名
    :param password: 密码
    :param cmd: 执行的命令
    :param seconds: 超时时间(默认)，必须是int类型
    :return: dict
    """
    logging.debug('{0} {1}'.format(host, cmd))
    result = {'code': 1, 'data': None}  # 返回结果
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, 22, user, password)  # 连接远程服务器,超时时间1秒
        stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)  # 执行命令
        out = stdout.read().decode()    # readlines会返回列表
        # 执行状态,0表示成功，1表示失败
        channel = stdout.channel
        status = channel.recv_exit_status()
        ssh.close()  # 关闭ssh连接

        # 修改返回结果，0表示成功，1表示失败
        result['code'] = status
        result['data'] = out
        return result
    except Exception as e:
        logging.error(str(type(e)) + ' ' + e)
        return False

if __name__ == '__main__':
    host = '120.78.123.249'
    user = 'root'
    password = 'Ali@123456'
    cmd = 'cd ~; ls'
    host = '192.168.111.254'
    user = 'zhaojinhui'
    password = '7075662'
    cmd = 'cd {}; ls'.format(
        '/Users/zhaojinhui/github/demz/material/commits'
    )
    r = ssh_exec_command(host, user, password, cmd)
    if r['code'] == 0:
        for commit in r['data'].split():
            logging.debug('commit:' + commit)
            tmp = os.path.join('/Users/zhaojinhui/github/demz/material/tmps', commit)
            os.makedirs(tmp)
            cmd = 'cat {}'.format(
                os.path.join('/Users/zhaojinhui/github/demz/material/commits', commit)
            )
            r = ssh_exec_command(host, user, password, cmd)
            if r['code'] == 0:
                logging.debug(r['data'].split())
                # 异步下载图片
                # 打包图片
                # 失败删除commit

            else:
                logging.error('CAT COMMIT FAIL')
                # 停止发送邮件
    else:
        logging.error('SCAN COMMITS FAIL')
        # 停止发送邮件









