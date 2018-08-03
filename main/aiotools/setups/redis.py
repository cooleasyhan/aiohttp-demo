try:
    import aioredis
except ImportError:
    pass


async def init_redis(app):

    conf = app['config']['redis']
    redis_pool = await aioredis.create_pool(
        conf['redis_url'],
        minsize=conf['minsize'], maxsize=conf['maxsize'])
    app['redis'] = redis_pool


async def close_redis(app):
    app['redis'].close()
    await app['redis'].wait_closed()


def setup_redis(app):
    try:
        import aioredis
    except ImportError:
        return
    app.on_startup.append(init_redis)
    app.on_cleanup.append(close_redis)
