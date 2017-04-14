# Copyright (C) Electronic Arts Inc.  All rights reserved.

from muffin.database import db

db_identifier = db.String(30)
db_metadata = db.String(None) # None means varchar(max)

# Identifiers are always 30 characters
# Metadata is VARCHAR(max) and should exist
# on every object that should support patching


projects_table = db.Table('projects',
                          db.Column('project_id', db.Integer, primary_key=True),
                          db.Column('name', db.String(150)),
                          info={'bind_key': None})

# shard_set contains information such as name, and other misc stuff.
# A shard_set points to another table with a list of all the shards it contains.
# A project points to one write shard_set and another read shard_set.
# Both read and write can point to the same shard_set.

# Test Suites

testsuite_table = db.Table('testsuite',
                           db.Column('id', db.Integer, primary_key=True),
                           db.Column('name', db_identifier),
                           db.Column('description', db.String(200)),
                           db.Column('metadata', db_metadata),
                           info={'bind_key': None})


testsuite_run_table = db.Table('testsuite_run',
                               db.Column('id', db.Integer, primary_key=True),
                               db.Column('testsuite_id', db.Integer, db.ForeignKey('testsuite.id')),
                               db.Column('createdAt', db.DateTime),
                               db.Column('metadata', db_metadata),
                               info={'bind_key': None})

testsuite_started_table = db.Table('testsuite_started',
                                   db.Column('id', db.Integer, primary_key=True),
                                   db.Column('testsuite_run_id', db.Integer, db.ForeignKey('testsuite_run.id')),
                                   db.Column('startedAt', db.DateTime),
                                   info={'bind_key': None})

testsuite_ended_table = db.Table('testsuite_ended',
                                 db.Column('id', db.Integer, primary_key=True),
                                 db.Column('testsuite_run_id', db.Integer, db.ForeignKey('testsuite_run.id')),
                                 db.Column('endedAt', db.DateTime),
                                 db.Column('result', db.Integer),
                                 info={'bind_key': None})

# Test suite tags

#TODO: Should tags use the name as their primary key?
#Seems we should at least have a unique key on the name to prevent duplicates

tag_table = db.Table('tag',
                     db.Column('id', db.Integer, primary_key=True),
                     db.Column('name', db_identifier),
                     db.Column('metadata', db_metadata),
                     info={'bind_key': None})

tagmappingtestsuite_table = db.Table('tag_mapping_testsuite',
                                     db.Column('id', db.Integer, primary_key=True),
                                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                                     db.Column('suite_id', db.Integer, db.ForeignKey('testsuite.id')),
                                     info={'bind_key': None})
