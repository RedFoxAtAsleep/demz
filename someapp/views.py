from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import logging
import asyncio
from .apps import COMMIT_DIR
from django.core.mail import get_connection, EmailMultiAlternatives, EmailMessage
from django.core.mail.backends.smtp import EmailBackend

backend_163 = EmailBackend(
        host='smtp.163.com',
        username='im22ic@163.com',
        password='wy123456',
    )

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create your views here.
import requests
import os
import time

STORE_PATH = '/Users/zhaojinhui/github/demz/material'


def index(request):
    logger.info('index')
    return HttpResponse('Welcome to someapp.')


async def download(request):
    begin = time.time()
    if request.method == 'GET':
        return HttpResponse('POST ONLY.')
    manner = request.POST.get('manner', None)
    if not manner:
        return HttpResponse('MANNER IS NEEDED, SYNC OR ASYNC')
    urls = request.FILES['urls'].read().decode().split()
    if len(urls) == 0:
        return HttpResponse('IMG URLS IS EMPTY')
    if str.lower(manner) == 'sync':
        for url in urls:
            await download_img(url)
        end = time.time()
        return HttpResponse('download finished, {}'.format(int(end-begin)))
    else:
        await download_imgs(urls)
        end = time.time()
        return HttpResponse('download finished, {}'.format(int(end-begin)))


async def download_img(url):
    try:
        file_name = str(time.time_ns()) + url[url.rindex(r'/') + 1:].split(r'?')[0]
        file_path = os.path.join(STORE_PATH, file_name)
        res = requests.get(url)
        with open(file_path, 'wb') as f:
            f.write(res.content)
    except Exception as e:
        logger.error(e)


def save_commit(request):
    # commit_time = time.strftime('%Y%m%d%H%M%S', time.gmtime())
    commit_time = str(time.time_ns())
    if request.method != 'POST':
        return HttpResponse('POST ONLY')
    urls = request.FILES.get('urls').read()
    try:
        logging.debug('SAVE COMMIT')
        f = open(os.path.join(COMMIT_DIR, commit_time), 'wb')
        f.write(urls)
        f.close()
        logging.debug('SAVE COMMIT SUCCESS')
        return JsonResponse({'code': 0})
    except Exception as e:
        logging.error(str(type(e)))
        logging.error(e)
        logging.error('SAVE COMMIT FAIL')
        return JsonResponse({'code': -1})


async def download_imgs(urls):
    await asyncio.gather(*[download_img(url) for url in urls])


def post(request):
    if request.method != "POST":
        return HttpResponse("POST ONLY".title())
    mail = request.POST.get("mail")
    hash_list = request.FILES.get("hash_list").read().decode()
    print(mail)
    print(hash_list)
    return JsonResponse({'content': hash_list})

def send_mail():
    subject, from_email, to = 'hello', 'im22ic()@163.com', 'rwjgzhjh@163.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # msg.content_subtype = "text"
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()



    # with get_connection(
    #         backend='demz.settings.backend_163'
    # ) as connection:
    #     EmailMessage(
    #         'subject1', 'body1', 'im22ic@163.com', ['rwjgzhjh@163.com'],
    #         connection=connection,
    #     ).send()
    with get_connection(
            host='smtp.163.com',
            username='im22ic@163.com',
            password='wy123456'
        ) as connection:
        EmailMessage(
            'subject1', 'body1', 'im22ic@163.com', ['rwjgzhjh@163.com'],
            connection=connection,
        ).send()


















