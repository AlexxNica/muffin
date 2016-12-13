# Copyright (C) Electronic Arts Inc.  All rights reserved.

from muffin.database import db
import muffin.tables as tables


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
    del databases['default']

    # setup rest
    binds = app.config['SQLALCHEMY_BINDS'] = {}
    for k, v in databases.items():
        binds[k] = _get_cs_from_db_binding(v)


def init_tables(drop_tables=False):  # pragma: no cover : init_tables is only used by seed and does nothing interesting
    db.reflect()

    if drop_tables:
        db.drop_all()

    db.create_all()


def insert_projects(projects):  # pragma: no cover : insert_projects is only used by seed and does nothing interesting
    engine = db.get_engine(app=None, bind=None)
    engine.execute(tables.projects_table.insert(), projects)


def init_app(app):
    _init_db_bindigs(app)
    db.init_app(app)
