import asyncio
import logging

logger = logging.getLogger(__name__)

task_conf_name = __name__


async def sleep(app):
    while True:
        logger.info('sleep...')
        await asyncio.sleep(10)


async def setup_jobs(app):
    app[task_conf_name] = (app.loop.create_task(
        sleep(app)),)


async def clean_jobs(app):
    for task in app[task_conf_name]:
        task.cancel()


def setup(app):
    logger.info('Register jobs')
    app.on_startup.append(setup_jobs)
    app.on_cleanup.insert(0, clean_jobs)
