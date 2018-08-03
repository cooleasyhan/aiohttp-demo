from .view import hello


def setup_routes(app, proj_root):
    router = app.router
    router.add_get('/hello', hello, name='hello')
