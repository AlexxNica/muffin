# Copyright (C) Electronic Arts Inc.  All rights reserved.

import random
from muffin.database import db
import muffin.tables as tables
from sqlalchemy.sql import select

shard_id_set = set([0])  # TODO we will need one set for each project in the future
shard_map = {0: "default"}


class BackendException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def _get_cs_from_db_binding(db_binding):
    db_type = db_binding.get('type', 'sqlite')
    driver = db_binding.get('driver', None)
    user = db_binding.get('user', '')
    password = db_binding.get('password', None)
    host = db_binding.get('host', None)
    db_name = db_binding.get('db', 'muffin')

    if db_type == 'sqlite':
        db_name += '.db'
        host = None

    # dialect+driver://username:password@host:port/database
    return "{}{}://{}{}{}/{}".format(
        db_type,
        ("+" + driver) if driver is not None else "",
        user,
        (":" + password) if password is not None else "",
        ("@" + host) if host is not None else "",
        db_name)


def _init_db_bindigs(app):

    if 'SQLALCHEMY_DATABASE_URI' in app.config:
        return

    if not app.config.get('DATABASES'):
        if not app.debug:
            app.logger.warn("""No databases specified in production mode.
            Will fall back to local sqlite instance.""")

    databases = app.config.get('DATABASES', {'default': {'db': "muffin"}})
    default_db = databases.get('default')

    if default_db is None:
        raise BackendException('No default database found.')

    # setup default db binding
    app.config['SQLALCHEMY_DATABASE_URI'] = _get_cs_from_db_binding(default_db)
    # TODO: Why are we doing this?
    # del databases['default']

    # setup rest
    binds = app.config['SQLALCHEMY_BINDS'] = {}
    for k, v in databases.items():
        binds[k] = _get_cs_from_db_binding(v)

    shard_map.update(app.config.get('SHARD_MAPPINGS', shard_map))
    shard_id_set.update(set(shard_map.keys()))


def init_tables(drop_tables=False):  # pragma: no cover
    # nocover - init_tables is only used by seed and does nothing interesting
    db.reflect()

    if drop_tables:
        db.drop_all()

    db.create_all()


def upsert_testsuite(entity_id, testsuite):
    """
    Upsert (insert/replace) the testsuite specified
    """
    sid = get_shard_id(entity_id)
    # db_id = get_db_id(entity_id)
    engine = _get_shard_engine(sid)

    # TODO: Do actual upsert
    new_record = engine.execute(tables.testsuite.insert(), testsuite)
    return new_record.inserted_primary_key[0]


def insert_testsuite_run(entity_id, testsuite_id, testsuite_run, started=None, ended=None):
    """
    insert a new run of a test suite, optionally specify the record for when it started and when it ended
    """
    # TODO: use test suite id?
    del testsuite_id

    sid = get_shard_id(entity_id)
    # db_id = get_db_id(entity_id)
    engine = _get_shard_engine(sid)

    new_run = engine.execute(tables.testsuite_run.insert(), testsuite_run)
    if started:
        engine.execute(tables.testsuite_started.insert(), started)
    if ended:
        engine.execute(tables.testsuite_ended.insert(), ended)
    return new_run.inserted_primary_key[0]


def insert_tags(tags, tag_mapping):
    engine = _get_shard_engine(sid=None)  # get default shard

    engine.execute(tables.tag.insert(), tags)
    engine.execute(tables.tagmappingtestsuite.insert(), tag_mapping)


def get_testsuites(entity_id, fields):
    sid = get_shard_id(entity_id)
    # db_id = get_db_id(entity_id)
    engine = _get_shard_engine(sid)

    # TODO: what to do with the db_id
    if fields:
        s = select([tables.testsuite.c[f] for f in fields])
    else:
        s = select([tables.testsuite])
    return engine.execute(s)


def get_testsuite(entity_id, testsuite_id, fields):
    sid = get_shard_id(entity_id)
    # db_id = get_db_id(entity_id)
    engine = _get_shard_engine(sid)

    # TODO: what to do with the db_id
    if fields:
        s = select([tables.testsuite.c[f] for f in fields])
    else:
        s = select([tables.testsuite])
    t = s.where(tables.testsuite.c.id == testsuite_id)
    return engine.execute(t).fetchone()


def get_testsuite_run(entity_id, testsuite_run_id, fields):
    sid = get_shard_id(entity_id)
    # db_id = get_db_id(entity_id)
    engine = _get_shard_engine(sid)

    # TODO: what to do with the db_id
    if fields:
        s = select([tables.testsuite_run.c[f] for f in fields])
    else:
        s = select([tables.testsuite_run])
    t = s.where(tables.testsuite_run.c.id == testsuite_run_id)
    return engine.execute(t).fetchone()

# def insert_projects(projects):
#     engine = _get_shard_engine(sid=None)  # get default shard
#     engine.execute(tables.projects.insert(), projects)


# example of how to get correct shard and id
# def get_testsuiterun(entity_id):
#     sid = get_shard_id(entity_id)
#     db_id = get_db_id(entity_id)
#     engine = _get_shard_engine(sid)
#
#      engine.execute(tables.testsuiteruns.select(), db_id)


def init_app(app):
    _init_db_bindigs(app)
    db.init_app(app)


def get_shard_id(entity_id):
    if entity_id is None:
        return None
    # first 32 bits are db id. 16 after is shard id. Rest is left for future.
    return (entity_id >> 32) & 0xffff


def get_db_id(entity_id):
    if entity_id is None:
        return None
    return entity_id & 0xffffffff


def build_entity_id(db_id, shard_id):
    return (shard_id << 32) | (db_id << 0)


# TODO Will need to pick correct shard set to randomize
def _generate_shard_id():  # pragma: no cover :
    return random.sample(shard_id_set, 1)


def _get_shard_engine(sid=None):  # pragma: no cover :
    return db.get_engine(app=None, bind=shard_map[sid] if sid is not None else None)
