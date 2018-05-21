# -*- coding: utf-8 -*-

import jwt
from aiohttp import web
from aiohttp_jwt import login_required

from ceres.db import Role
from ceres.users import list_users


__all__ = (
    'routes',
    'api_routes',
)


routes = web.RouteTableDef()
api_routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
    return web.json_response(data={'status': 'ok'})


@routes.post('/auth')
async def authenticate(request: web.Request) -> web.Response:
    """
    View is used to authenticate a user
    """
    conf = request.app['config']
    form = await request.post()

    username = form.getone('username', None)
    password = form.getone('password', None)

    if username is None:
        return web.json_response(data={'error': 'forbidden'}, reason='forbidden', status=403)

    if password is None:
        return web.json_response(data={'error': 'forbidden'}, reason='forbidden', status=403)

    # TODO: authenticate a user

    token = jwt.encode({'username': username, 'scopes': ['role:' + Role.SENIOR.value]}, conf.sharable_secret)

    return web.json_response(
        data={'token': token.decode('utf-8')},
        headers={'Authorization': 'Bearer {}'.format(token.decode('utf-8'))})


@api_routes.get('/users')
@login_required
async def get_list_users(request):
    users = await list_users(request.app['db'])
    return web.json_response({'users': users, })
