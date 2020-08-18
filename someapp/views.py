from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import logging
import asyncio


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


async def download_imgs(urls):
    await asyncio.gather(*[download_img(url) for url in urls])
















