# Copyright (C) Electronic Arts Inc.  All rights reserved.

from muffin.database import db

projects_table = db.Table('projects',
                          db.Column('project_id', db.Integer, primary_key=True),
                          db.Column('name', db.String(150)),
                          info={'bind_key': None})
