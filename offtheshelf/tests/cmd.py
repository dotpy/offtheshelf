"""Command for running unit tests for the module from setup.py"""

from distutils.cmd import Command
from unittest import TextTestRunner, TestLoader

import offtheshelf.tests


class TestCommand(Command):
    """Command for running unit tests for the module from setup.py"""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        suite = TestLoader().loadTestsFromModule(offtheshelf.tests)
        TextTestRunner(verbosity=1).run(suite)
