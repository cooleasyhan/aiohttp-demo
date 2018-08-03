#!/usr/bin/env python
"""
    Worker example from the 2nd tutorial
"""

import asyncio
import sys

import aioamqp

from aiotools.mq import Mq


async def callback(channel, body, envelope, properties):
    print(" [x] Received %r" % body)
    await asyncio.sleep(body.count(b'.'))
    print(" [x] Done")
    await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)


async def worker(mq):

    channel = await mq.get_channel()

    await channel.queue(queue_name='test', durable=True)
    await channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)
    await channel.basic_consume(callback, queue_name='test')

conf = {
    'host': '127.0.0.1',
    'port': 5672,
    # 'login': 'x',
    # 'password': 'x',
    'virtualhost': '/',
    'heartbeat': 60}

mq = Mq(**conf)


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(worker(mq))
event_loop.run_forever()
