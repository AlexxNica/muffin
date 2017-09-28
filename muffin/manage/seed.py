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

        customer_id = None
        first_suite = backend.upsert_testsuite(customer_id,
                                               {
                                                   "name": "TestSuite Name",
                                                   "description": "A cool description",
                                                   "metadata": "{}"
                                               })
        second_suite = backend.upsert_testsuite(customer_id,
                                                {
                                                    "name": "Another testsuite",
                                                    "description": "A boring description",
                                                    "metadata": str(json.dumps({"platform": "windows"}))
                                                })

        # a completed succesful run
        backend.insert_testsuite_run(customer_id, first_suite,
                                     {
                                         "createdAt": datetime.datetime.now(),
                                         "metadata": str(json.dumps({"build_version_id": "1337"}))
                                     },
                                     {
                                         "startedAt": datetime.datetime.now(),
                                     },
                                     {
                                         "endedAt": datetime.datetime.now(),
                                         "result": 0  # succesful
                                     })

        # a failed finished run
        backend.insert_testsuite_run(customer_id, first_suite,
                                     {
                                         "createdAt": datetime.datetime.now(),
                                         "metadata": str(json.dumps({"build_version_id": "1338"}))
                                     },
                                     {
                                         "startedAt": datetime.datetime.now(),
                                     },
                                     {
                                         "endedAt": datetime.datetime.now(),
                                         "result": 1  # failed
                                     })

        # running run
        backend.insert_testsuite_run(customer_id, first_suite,
                                     {
                                         "createdAt": datetime.datetime.now(),
                                         "metadata": str(json.dumps({"build_version_id": "1338"}))
                                     },
                                     {
                                         "startedAt": datetime.datetime.now(),
                                     },
                                     None)

        # run that has yet to start
        backend.insert_testsuite_run(customer_id, second_suite,
                                     {
                                         "createdAt": datetime.datetime.now(),
                                         "metadata": str(json.dumps({"build_version_id": "1338"}))
                                     },
                                     None,
                                     None)

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
