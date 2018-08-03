import asyncio
import logging

import aioamqp

logger = logging.getLogger(__name__)


class Mq:
    def __init__(self, **kwargs):
        self.conf = kwargs
        if 'heartbeat' in self.conf:
            self.heartbeat = self.conf.pop('heartbeat')
        else:
            self.heartbeat = None
        self.transport = None
        self.protocol = None
        self.connection_lock = asyncio.Lock()
        self.channel_lock = asyncio.Lock()
        self.channel = None
        self.re_connect_event = asyncio.Event()
        self.channel_re_create_event = asyncio.Event()

    async def _connect(self):
        logger.info('Creating amqp connection to %s:%s' %
                    (self.conf['host'], self.conf['port']))
        self.transport, self.protocol = await aioamqp.connect(
            **self.conf
        )

    async def close_connection(self):
        if self.transport or self.protocol:
            try:
                await self.protocol.close()
                self.transport.close()
                await self.protocol.wait_closed(timeout=1)
            except:
                pass
            finally:
                self.transport = None
                self.protocol = None

    async def re_connect(self):
        self.re_connect_event.set()
        await self.close_connection()
        await self._connect()
        self.re_connect_event.clear

    async def get_connection(self):
        async with self.connection_lock:
            try:
                await self.protocol.ensure_open()
            except:
                await self.re_connect()
            return self.transport, self.protocol

    async def close_channel(self):
        if self.channel:
            try:
                await self.channel.close()
            except:
                pass
            finally:
                self.channel = None

    async def _channel(self):
        transport, protocol = await self.get_connection()
        self.channel = await self.protocol.channel()

    async def get_channel(self):
        async with self.channel_lock:
            if self.channel:
                try:
                    await self.protocol.ensure_open()
                    self.channel_re_create_event.clear()
                    if self.channel.is_open:
                        return self.channel
                except:
                    self.close_channel()

            self.channel_re_create_event.set()
            logger.info('Creating amqp channel')
            transport, protocol = await self.get_connection()
            await self._channel()

        return self.channel

    async def start_heartbeat(self):
        if self.heartbeat is None:
            return
        try:
            transport, protocol = self.get_connection()
            while True:
                # issue manual heartbeat every 20 seconds
                await asyncio.sleep(int(self.heartbeat))
                logger.info('AMQP_Task1: Send Out HeartBeat')
                await self.protocol.send_heartbeat()
        except asyncio.CancelledError:
            pass

    async def handle_closed(self):
        try:

            logger.info('AMQP_Task2: Start Handler AMQP Close')
            while True:
                await self.protocol.wait_closed()
                logger.info(
                    'AMQP_Task2: AMQP Connection Lost, Try to Reconnect')
                await self.re_connect()
        except asyncio.CancelledError:
            pass
