from django.test import TestCase

# Create your tests here.

import asyncio
import threading
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging


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

if __name__ == '__main__':

    print("Main runs in %s" % (threading.current_thread(),))
    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.start()
    scheduler.add_job(my_coroutine, 'interval', seconds=2)
    loop.run_forever()