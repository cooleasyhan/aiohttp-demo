import logging
import time

import aioamqp
from aiohttp import web

logger = logging.getLogger(__name__)


async def publish(request):
    s = time.time()
    app = request.app

    mq = app['amqp']
    exchange = 'test'
    routing_key = 'test'
    if mq.channel:
        channel = mq.channel
    else:
        mq.channel = await mq.get_channel()

    # await channel.queue_bind('test', 'test', 'test')
    # await channel.queue_declare("test", durable=True)
    i = 10
    while i:
        try:
            await channel.publish("aioamqp hello"*10, 'test', "test")
        except Exception as e:
            logger.exception(e)
            channel = await mq.get_channel()

        i -= 1
    e = time.time()
    return web.Response(text='ok' + str(e-s))


async def basic_get(request):
    s = time.time()
    app = request.app
    mq = app['amqp']
    channel = await mq.get_channel()
    i = 1
    while i:
        try:
            x = await channel.basic_get('test')
            await channel.basic_client_ack(delivery_tag=x['delivery_tag'])
        except Exception as e:
            logger.exception(e)
            channel = await mq.get_channel()
        i -= 1
    e = time.time()
    return web.Response(text='ok' + str(e-s))
