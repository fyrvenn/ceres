# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
from sqlalchemy import select, desc, create_engine

from ceres import db
from ceres import users


@pytest.fixture
def make_db_schema(pg_params):
    db_string = "postgres://{user}:{password}@{host}:{port}/{database}".format(**pg_params)
    engine = create_engine(db_string)
    db.metadata.create_all(engine)

    yield True

    db.metadata.drop_all(engine)


@pytest.fixture
async def sample_users(make_sa_connection, make_db_schema):
    conn = await make_sa_connection()
    await conn.execute(db.users.insert().values(name='user1', role=db.Role.SENIOR, password='ece221df5b9725ad1382b44abb635ac582636587b8b03b7d7dae3f3ae727f9b5d045f823ed41aa159a45abecfc20a6499535b58c1e4e6902d2d8a166eeca0b50:fd908c4ed195418893893f7c9d70bcdc')) # password1
    await conn.execute(db.users.insert().values(name='user2', role=db.Role.SENIOR, password='caedc41bf2b9f30bda01374b9af8e031bff56c60be078fd387f6b40f3da433102c3214f70971adf4ff7680a281a72f697ce26823ec1dabcc9d3a2460d08514d1:fd908c4ed195418893893f7c9d70bcdc')) # password2
    await conn.execute(db.users.insert().values(deleted_on=datetime.now(), name='user3', role=db.Role.ASSISTANT, password='52c4b104230319f6c1e3ae870cc2b2fe9abf5369c8f168e38a0d52dff1309c42671cf7ce14f1dc7fcf7ce36676e81875c6da95dec16aa4acfb9649926a1d8b1c:fd908c4ed195418893893f7c9d70bcdc')) #password3
    return True


async def test_sample_query(make_sa_connection, sample_users):

    import pdb
    pdb.set_trace()

    """
    This is an example of how one can create a unit test which uses aiopg and dockerized postgres server
    """
    connection = await make_sa_connection()

    query = select([db.users.c.id, db.users.c.name, db.users.c.role]).order_by(desc(db.users.c.id))
    rows = []
    async for row in connection.execute(query):
        rows.append(row)

    assert len(rows) == 3, 'the query must return all records from the users database table'

    query = query.offset(0).limit(2)
    rows = []
    async for row in connection.execute(query):
        rows.append(row)

    assert len(rows) == 2, 'the query must return two rows'


# async def test_authenticate(make_engine, sample_users):
#     engine = await make_engine()
#
#     user = await users.authenticate(engine, 'user1', 'password1')
#     assert user is not None, 'authenticate should return a user if its password matches the one provided'
#
#     user = await users.authenticate(engine, 'user1', 'passwordX')
#     assert user is None, 'authenticate should return None if the password is wrong'
#
#     user = await users.authenticate(engine, 'userX', 'password1')
#     assert user is None, 'authenticate should return None if a user does not exists'
#
#     user = await users.authenticate(engine, 'user3', 'password3')
#     assert user is None, 'authenticate should return None if a user was deleted'


# async def test_list_users(make_engine, sample_users):
#     pass
