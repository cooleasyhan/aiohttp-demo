import asyncio

from aiotools.app import PROJ_ROOT, TEMPLATES_ROOT
from aiotools.app import get_app as aio_get_app
from aiotools.utils import load_job, load_router

installed_apps = ['demo', ]


async def setup(app):
    for installed_app in installed_apps:
        load_job(app, installed_app)
        load_router(app, installed_app, PROJ_ROOT)


async def get_app():
    app = await aio_get_app()
    await setup(app)

    return app
