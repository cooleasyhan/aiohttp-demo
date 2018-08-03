
try:
    import aiomysql
except ImportError:
    pass


async def init_mysql(app):
    conf = app['config']['mysql']
    engine = await aiomysql.create_pool(
        db=conf['db'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_mysql(app):
    app['db'].close()
    await app['db'].wait_closed()


def setup_mysql(app):
    try:
        import aiomysql
    except ImportError:
        return
    app.on_startup.append(init_mysql)
    app.on_cleanup.append(close_mysql)
