# -*- coding: utf-8 -*-

import asyncio
import platform
import psycopg2
import pytest
import socket
import time
import uuid

import docker as docker_api

from aiopg import sa


@pytest.fixture(scope='session')
def unused_port():
    if platform.system() == 'Darwin' or platform.system() == 'Windows':
        return lambda: 5433
    else:
        def f():
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', 0))
                return s.getsockname()[1]

        return f


@pytest.fixture(scope='session')
def docker():
    return docker_api.from_env()


@pytest.fixture(scope='session')
def session_id():
    return str(uuid.uuid4())


@pytest.fixture(scope='session')
def pg_server(unused_port, docker, session_id):

    docker.api.pull('postgres:alpine')

    container_args = dict(
        image='postgres:alpine',
        name='ceres-test-db-{}'.format(session_id),
        ports=[5432],
        detach=True,
    )

    host = "127.0.0.1"
    host_port = unused_port()
    container_args['host_config'] = docker.api.create_host_config(port_bindings={5432: ('0.0.0.0', host_port)})

    container = docker.api.create_container(**container_args)

    try:
        docker.api.start(container=container['Id'])
        server_params = dict(database='postgres',
                             user='postgres',
                             password='mysecretpassword',
                             host=host,
                             port=host_port)

        delay = 0.001
        for i in range(100):
            try:
                conn = psycopg2.connect(**server_params)
                cur = conn.cursor()
                cur.execute("CREATE EXTENSION hstore;")
                cur.close()
                conn.close()
                break
            except psycopg2.Error as err:
                print(err)
                time.sleep(delay)
                delay *= 2
        else:
            pytest.fail("Cannot start postgres server")

        container['host'] = host
        container['port'] = host_port
        container['pg_params'] = server_params

        yield container
    finally:
        docker.api.kill(container=container['Id'])
        docker.api.remove_container(container['Id'])


@pytest.fixture
def pg_params(pg_server):
    return dict(**pg_server['pg_params'])


@pytest.fixture
def make_engine(loop, pg_params):
    engine = None

    @asyncio.coroutine
    def go(*, use_loop=True, **kwargs):
        pg_params.update(kwargs)
        if use_loop:
            engine = yield from sa.create_engine(loop=loop, **pg_params)
        else:
            engine = yield from sa.create_engine(**pg_params)
        return engine

    yield go

    if engine is not None:
        engine.close()
        loop.run_until_complete(engine.wait_closed())


@pytest.fixture
def make_sa_connection(make_engine):
    conn = None
    engine = None

    @asyncio.coroutine
    def func(*, use_loop=True, **kwargs):
        nonlocal conn, engine
        engine = yield from make_engine(use_loop=use_loop, **kwargs)
        conn = yield from engine.acquire()
        return conn

    yield func

    if conn is not None:
        engine.release(conn)
