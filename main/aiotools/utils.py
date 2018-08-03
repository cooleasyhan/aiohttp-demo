import importlib

import yaml
from aiohttp import web


def load_config(fname):
    with open(fname, 'rt') as f:
        data = yaml.load(f)
    # TODO: add config validation
    return data


def load_router(app, pkg, proj_root):
    m = importlib.import_module('%s.routes' % pkg)
    function = getattr(m, 'setup_routes')
    function(app, proj_root)


def load_job(app, pkg):
    m = importlib.import_module('%s.jobs' % pkg)
    function = getattr(m, 'setup')
    function(app)


def redirect(request, name, **kw):
    router = request.app.router
    location = router[name].url(**kw)
    return web.HTTPFound(location=location)
