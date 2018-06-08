import aiopg.sa
from datetime import datetime
from enum import Enum
from logging import getLogger
import sqlalchemy as sa


__all__ = (
    'Role',
    'init_db',
    'users',
    'projects',
    'projects_staff',
)


class Role(Enum):
    SENIOR = 'senior'
    ASSISTANT = 'assistant'


metadata = sa.MetaData()


users = sa.Table('users', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('name', sa.String(255), unique=True),
    sa.Column('role', sa.Enum(Role), default=Role.SENIOR),
    sa.Column('password', sa.String(255), nullable=False),
    sa.Column('created_on', sa.DateTime(), default=datetime.now),
    sa.Column('updated_on', sa.DateTime(), default=datetime.now, onupdate=datetime.now),
    sa.Column('deleted_on', sa.DateTime(), nullable=True)
)


projects = sa.Table('projects', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('name', sa.String(255), unique=True),
    sa.Column('user_id', sa.ForeignKey('users.id')),
    sa.Column('created_on', sa.DateTime(), default=datetime.now),
    sa.Column('updated_on', sa.DateTime(), default=datetime.now, onupdate=datetime.now),
    sa.Column('deleted_on', sa.DateTime(), nullable=True)
)


projects_staff = sa.Table('projects_staff', metadata,
    sa.Column('project_id', sa.ForeignKey('projects.id')),
    sa.Column('user_id', sa.ForeignKey('users.id')),
    sa.Column('created_on', sa.DateTime(), default=datetime.now),
    sa.Column('deleted_on', sa.DateTime(), nullable=True),
    sa.Index('ix_projects_staff', 'project_id', 'user_id', unique=True)
)


async def init_db(app):
    log = getLogger(__name__)
    log.info('initializing the database connection pool')
    conf = app['config']
    engine = await aiopg.sa.create_engine(
        database=conf.db_name,
        user=conf.db_user,
        password=conf.db_password,
        host=conf.db_host,
        port=conf.db_port,
        minsize=conf.db_minsize,
        maxsize=conf.db_maxsize,
        loop=app.loop)
    log.info('database connection pool is initialized')
    app['db'] = engine
    yield
    log.info('closing database connection pool')
    engine.close()
    await engine.wait_closed()
    log.info('database connection pool is closed')
