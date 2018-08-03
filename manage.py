import asyncio
import logging
import os
import sys

import click
from aiohttp import web


@click.command()
@click.option('--host', default='127.0.0.1', help='Binding Host')
@click.option('--port', default='9001', help='Binding Port')
@click.option('--debug', default=False, help='Debug Flag')
def main(host, port, debug):
    from main.app import get_app
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(get_app())
    if debug:
        import aiohttp_debugtoolbar
        aiohttp_debugtoolbar.setup(app)
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(current_path, 'main'))
    main()
