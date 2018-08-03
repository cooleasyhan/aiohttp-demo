import logging
import time

import aioamqp
from aiohttp import web

logger = logging.getLogger(__name__)


async def hello(request):
    return web.Response(text='Hello World')
