import asyncio
import logging
import pathlib

import click
from aiohttp import web

from aiotools.setups.amqp import setup_amqp
from aiotools.setups.mysql import setup_mysql
from aiotools.setups.redis import setup_redis
from aiotools.setups.routes import setup_routes
from aiotools.utils import load_config, load_job, load_router

PROJ_ROOT = pathlib.Path(__file__).parent.parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'


async def setup(app, loop):
    conf = load_config(PROJ_ROOT / 'config' / 'config.yml')

    app.update(
        name='main',
        config=conf
    )

    setup_amqp(app)
    setup_redis(app)
    setup_mysql(app)

    setup_routes(app, PROJ_ROOT)
    return app


async def get_app(app=None, loop=None):
    if app is None:
        app = web.Application(loop=loop)
    if loop is None:
        loop = asyncio.get_event_loop()
    app = await setup(app, loop)
    return app
