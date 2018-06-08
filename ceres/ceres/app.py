# -*- coding: utf-8 -*-

import logging

from aiohttp import web
from aiohttp_jwt import JWTMiddleware

from ceres.config import Config
from ceres.resources import routes, api_routes
from ceres.db import init_db


__all__ = (
    'make_app',
    'run_app',
)


def make_app(conf, initialize_db):
    api = web.Application(
        middlewares=[
            JWTMiddleware(
                secret_or_pub_key=conf.sharable_secret,
                request_property='user',
                credentials_required=False,
            ),
        ]
    )
    api['config'] = conf
    api.add_routes(api_routes)
    api.cleanup_ctx.append(initialize_db)

    app = web.Application()
    app.add_routes(routes)
    app.add_subapp('/api/v1', api)
    return app


def run_app():
    conf = Config()
    logging.basicConfig(level=logging.DEBUG)
    app = make_app(conf, init_db)
    web.run_app(app, host=conf.host, port=conf.port)
