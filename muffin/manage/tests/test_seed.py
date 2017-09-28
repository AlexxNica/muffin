# Copyright (C) Electronic Arts Inc.  All rights reserved.


import flask_script
import muffin.manage.seed as mg


def test_seed(app):
    """
    Run the seed command on a in memory database to verify its working
    """

    manager = flask_script.Manager(app)
    manager.add_command('seed', mg.SeedDatabase)

    result = manager.handle(__file__, ['seed'])

    assert not result
