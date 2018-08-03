import asyncio
import logging
from functools import partial

from aiotools.mq import *

try:
    import aioamqp
except ImportError:
    pass


async def init_amqp(app):
    conf = app['config']['amqp']
    mq = Mq(**conf)
    await mq.re_connect()
    app['amqp'] = mq


async def close_amqp(app):
    mq = app['amqp']
    await mq.close_channel()
    await mq.close_connection()


async def heartbeat(app):
    mq = app['amqp']
    await mq.start_heartbeat()


async def handle_closed(app):
    mq = app['amqp']
    await mq.handle_closed()


async def setup_jobs(app):
    app['amqp_tasks'] = (app.loop.create_task(
        heartbeat(app)), app.loop.create_task(handle_closed(app)))


async def clean_jobs(app):
    for task in app['amqp_tasks']:
        task.cancel()


def setup_amqp(app):
    try:
        import aioamqp
    except ImportError:
        return

    app.on_startup.append(init_amqp)
    app.on_startup.append(setup_jobs)
    app.on_cleanup.append(close_amqp)
    app.on_cleanup.append(clean_jobs)
