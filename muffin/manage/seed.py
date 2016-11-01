import time
import random
from flask_script import Command
from faker import Faker
import muffin.backend as backend


class SeedDatabase(Command):
    # command method
    def run(self):  # pylint: disable=E0202
        print("seeding database...")
        start = time.clock()
        random.seed(123)
        print("done, elapsed time: {}s".format((time.clock() - start)))
