# -*- coding: utf-8 -*-

import pytest
from unittest import mock

from aiopg import sa

from ceres.config import Config
from ceres.app import make_app


async def stub_init_db(app):
    app['db'] = mock.Mock(from_spec=sa.engine.Engine)
    yield
    app['db'] = None


@pytest.fixture
def cli(loop, aiohttp_client):
    app = make_app(Config(), stub_init_db)
    return loop.run_until_complete(aiohttp_client(app))


async def test_index(cli):
    resp = await cli.get('/')

    assert resp.status == 200

    data = await resp.json()

    expected = {'status': 'ok'}
    assert all(True for key in expected if key in data) and all(True for key in data if key in expected)
