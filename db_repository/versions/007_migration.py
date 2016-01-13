from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
request_to__app = Table('request_to__app', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('request_time', DateTime),
    Column('method', String),
    Column('path_info', String),
    Column('server_protocol', String),
    Column('server_address', String),
    Column('server_port', String),
    Column('viewed', Boolean),
)

request_to_app = Table('request_to_app', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('request_time', DateTime),
    Column('method', String(length=5)),
    Column('path_info', String(length=200)),
    Column('server_protocol', String(length=10)),
    Column('server_address', String(length=50)),
    Column('server_port', String(length=5)),
    Column('viewed', Boolean, default=ColumnDefault(False)),
)

note = Table('note', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('notes', String),
    Column('image_path', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['request_to__app'].drop()
    post_meta.tables['request_to_app'].create()
    pre_meta.tables['note'].columns['image_path'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['request_to__app'].create()
    post_meta.tables['request_to_app'].drop()
    pre_meta.tables['note'].columns['image_path'].create()
