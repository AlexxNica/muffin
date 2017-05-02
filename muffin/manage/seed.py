# Copyright (C) Electronic Arts Inc.  All rights reserved.

import time
import random
import datetime
import json
from flask_script import Command
import flask
import muffin.backend as backend


class SeedDatabase(Command):
    # command method
    def run(self):  # pylint: disable=E0202
        app = flask.current_app
        random.seed(123)

        print("seeding database...")
        start = time.clock()
        backend.init_app(app)
        backend.init_tables(drop_tables=True)

        # backend.insert_projects()

        backend.insert_testsuites([
            {
                "name": "TestSuite Name",
                "description": "A cool description",
                "metadata": "{}"
            },
            {
                "name": "Another testsuite",
                "description": "A boring description",
                "metadata": str(json.dumps({"platform": "windows"}))
            }
        ])

        backend.insert_runs(
            [
                # a completed succesful run
                (
                    {
                        "id": 1,
                        "testsuite_id": 1,
                        "createdAt": datetime.datetime.now(),
                        "metadata": str(json.dumps({"build_version_id": "1337"}))
                    },
                    {
                        "testsuite_run_id": 1,
                        "startedAt": datetime.datetime.now(),
                    },
                    {
                        "testsuite_run_id": 1,
                        "endedAt": datetime.datetime.now(),
                        "result": 0  # succesful
                    }
                ),
                # a failed finished run
                (
                    {
                        "id": 2,
                        "testsuite_id": 1,
                        "createdAt": datetime.datetime.now(),
                        "metadata": str(json.dumps({"build_version_id": "1338"}))
                    },
                    {
                        "testsuite_run_id": 2,
                        "startedAt": datetime.datetime.now(),
                    },
                    {
                        "testsuite_run_id": 2,
                        "endedAt": datetime.datetime.now(),
                        "result": 1  # failed
                    }
                ),
                # running run
                (
                    {
                        "id": 3,
                        "testsuite_id": 1,
                        "createdAt": datetime.datetime.now(),
                        "metadata": str(json.dumps({"build_version_id": "1338"}))
                    },
                    {
                        "testsuite_run_id": 3,
                        "startedAt": datetime.datetime.now(),
                    },
                    None
                ),
                # run that has yet to start
                (
                    {
                        "id": 4,
                        "testsuite_id": 1,
                        "createdAt": datetime.datetime.now(),
                        "metadata": str(json.dumps({"build_version_id": "1338"}))
                    },
                    None,
                    None
                )
            ]
        )

        backend.insert_tags(
            [{"tag_id": 1, "name": "Mantle", "metadata": "{}"}],
            [{"tag_id": 1, "suite_id": 1}]
        )

        # for i in range(0,4):
        #    # the first 4 runs are all for the same test suite
        #    backend.insert_tests(
        #        [
        #
        #        ])

        print("done, elapsed time: {}s".format((time.clock() - start)))
