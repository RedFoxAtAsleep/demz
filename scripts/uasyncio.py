# -*- coding: utf-8 -*-
import asyncio
import time
from threading import Thread
from functools import partial
import traceback


async def async_f(x, t):
    start_pt = time.process_time()
    start_in = time.perf_counter()
    print('async f start {0}'.format(x))
    await asyncio.sleep(t)  # asyncio.sleep(0)也会出让执行权
    print('async f end {0}, in time: {1}, process time: {2}'.format(
        x,
        start_in - time.perf_counter(),
        start_pt - time.process_time())
    )
    return x*t


async def blocked_async_f(x, t):
    start_pt = time.process_time()
    start_in = time.perf_counter()
    print('blocked async f start {0}'.format(x))
    time.sleep(t)  # asyncio.sleep(0)也会出让执行权
    print('blocked async f end {0}, in time: {1}, process time: {2}'.format(
        x,
        start_in - time.perf_counter(),
        start_pt - time.process_time())
    )
    return x*t


def f(x, t):
    start_pt = time.process_time()
    start_in = time.perf_counter()
    print('sync f start {0}'.format(x))
    time.sleep(t)  # asyncio.sleep(0)也会出让执行权
    print('sync end {0}, in time: {1}, process time: {2}'.format(
        x,
        start_in - time.perf_counter(),
        start_pt - time.process_time())
    )
    return x * t


async def main00():
    # asyncio.gather 用来并发运行任务
    # asyncio.gather() is an awaitable itself, await is needed to deal with
    # [resutls =] await asyncio.gather()

    print('main 00')
    start_pt = time.process_time()
    start_in = time.perf_counter()
    resutls = await asyncio.gather(async_f('a', 1), async_f('b', 1), blocked_async_f('c', 1), async_f('d', 1))
    print(resutls)
    print('main 00, in time: {0}, process time: {1}'.format(
        start_in - time.perf_counter(),
        start_pt - time.process_time())
    )


async def main01():
    print('main 01')
    start_pt = time.process_time()
    start_in = time.perf_counter()
    done, pending = await asyncio.wait([async_f('a', 1), async_f('b', 1), blocked_async_f('c', 1), async_f('d', 1)])
    print([task.result() for task in done])
    print([task.result() for task in pending])
    print('main 01, in time: {0}, process time: {1}'.format(
        start_in - time.perf_counter(),
        start_pt - time.process_time())
    )


async def main02():
    print('main 02')
    start_pt = time.process_time()
    start_in = time.perf_counter()

    # asyncio.create_task 包装 coroutine 成为 task
    await asyncio.create_task(async_f('o', 1))  # 只有1个可等待对象，无并发
    await asyncio.create_task(async_f('p', 1))  # 只有1个可等待对象，无并发
    # _ = await asyncio.create_task(async_f('o', 1))
    # _ = await asyncio.create_task(async_f('p', 1))

    task1 = asyncio.create_task(async_f('r', 2))
    task2 = asyncio.create_task(async_f('s', 1))
    # 有2个可等待的对象
    # task 执行 挂起 执行
    await task1
    # 不考虑轮转时间片：task1执行、task1挂起、task2执行、task2挂起、task1执行、task2执行
    # 轮转时间片，task1挂起时间更长：task1执行、task2执行、task1挂起、task2挂起、task2执行、task1执行
    # 轮转时间片，task2挂起时间更长：task1执行、task2执行、task1挂起、task2挂起、task1执行、task2执行
    # 轮转时间片，挂起时间一样长：task1执行、task2执行、task1挂起、task2挂起、task1执行、task2执行
    print('-'*10)
    await task2

    coroutine = async_f('x', 1)  # 同步阻塞代码，只有1个可等待对象
    asyncio.create_task(async_f('y', 3))  # 同步阻塞代码，只有
    asyncio.create_task(async_f('z', 5))  # 同步阻塞代码

    time.sleep(1)  # 同步阻塞代码，并不会交出控制权，异步任务得不到执行权
    await asyncio.sleep(0)  # 交出CPU执行权，但交出的瞬间就取回
    await coroutine

    for i in range(3):
        await asyncio.sleep(1)

    print('main 02, in time: {0}, process time: {1}'.format(
        start_in - time.perf_counter(),
        start_pt - time.process_time())
    )  # 同步阻塞代码


async def main03():
    rs = asyncio.gather(async_f('x', 1), async_f('y', 1))
    await rs
    print(type(rs))

    asyncio.gather(async_f('x', 1), async_f('y', 1))
    await asyncio.gather(async_f('x', 1), async_f('y', 1))


async def main04():
    rs = asyncio.gather(async_f('x', 1), async_f('y', 1))
    await rs
    print(type(rs))

    await asyncio.gather(async_f('x', 1), async_f('y', 1))
    try:
        asyncio.gather(async_f('x', 1), async_f('y', 1))
    except:
        print('在获得可等待对象后没有/不曾切换到事件循环异步模式')
        print('会有警告 RuntimeWarning: coroutine ... was never awaited')


def main05():

    def start_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def shutdown(loop):
        loop.stop()

    new_loop = asyncio.new_event_loop()
    t = Thread(target=start_loop, args=(new_loop,))
    t.start()

    future = asyncio.run_coroutine_threadsafe(async_f('x', 3), new_loop)
    for i in range(3):
        time.sleep(1)
        print(future)
    new_loop.call_soon_threadsafe(partial(shutdown, new_loop))

if __name__ == '__main__':
    # 从普通函数到Future对象
    loop = asyncio.get_event_loop()
    f_future = loop.run_in_executor(None, f)
    # print([(attr, type(getattr(f, attr))) for attr in dir(f) if not attr.startswith('_')])
    # print([(attr, type(getattr(async_f, attr))) for attr in dir(async_f) if not attr.startswith('_')])
    # print([(attr, type(getattr(async_f('x', 1), attr))) for attr in dir(async_f('x', 1)) if not attr.startswith('_')])
    # print([(attr, type(getattr(f_future, attr))) for attr in dir(f_future) if not attr.startswith('_')])

    # asyncio.run(main00())
    # asyncio.run()是同步代码
    # asyncio.run是Python3.7新加的接口，要不然你得这么写:
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()

    # asyncio.run(main01())

    # asyncio.run(main02())

    asyncio.create_task(f('x',2))
    asyncio.gather(async_f('x', 1), async_f('xx', 1), async_f('xxx', 1))
    loop = asyncio.get_event_loop()
    # loop.run_forever()


    # try:
    #     asyncio.get_running_loop()
    # except Exception as e:
    #     print(traceback.format_exc())
    #
    # loop = asyncio.get_event_loop()
    # # loop <_UnixSelectorEventLoop running=False closed=False debug=False>
    #
    # try:
    #     asyncio.get_event_loop()
    # except:
    #     print(traceback.format_exc())
    #
    # asyncio.run(main04())
    # try:
    #     asyncio.get_running_loop()
    # except Exception as e:
    #     print(traceback.format_exc())
    #
    # try:
    #     asyncio.get_event_loop()
    # except:
    #     print(traceback.format_exc())
    #
    # try:
    #     loop = asyncio.new_event_loop()
    #     asyncio.get_event_loop()
    # except:
    #     print(traceback.format_exc())
    #
    # try:
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     loop.run_until_complete(async_f('x', 1))  # loop.close
    #     asyncio.get_event_loop()
    #     asyncio.get_running_loop()
    # except:
    #     print(traceback.format_exc())


    # main05()


    # Coroutine，本质上是一个函数，可以交出执行权给其他协程，协程函数返回协程对象
    # Eventloop，时间循环，时间循环和线程的关系？？？
    # Future，异步操作结束后会把最终结果设置到 Future 对象上。Future 是对协程的封装。









