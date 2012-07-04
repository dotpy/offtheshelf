#!/usr/bin/env python


"""
This is the installation script of the offtheshelf module, a very simple and
minimal NoSQL database that uses shelve as a backend. You can run it by typing:

  python setup.py install

You can also run the test suite by running:

  python setup.py test
"""


import sys
from distutils.core import setup
from offtheshelf.tests import TestCommand


__author__ = "Daniele Mazzocchio <danix@kernel-panic.it>"
__version__ = "0.0.1"
__date__    = "Jun 24, 2012"


# Python versions prior 2.2.3 don't support 'classifiers' and 'download_url'
if sys.version < "2.2.3":
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name         = "offtheshelf",
      version      = __version__,
      author       = "Daniele Mazzocchio",
      author_email = "danix@kernel-panic.it",
      packages     = ["offtheshelf"],
      cmdclass     = {"test": TestCommand},
      description  = "Simple NoSQL database with shelve backend",
      classifiers  = ["Development status :: 2 - Pre-Alpha",
                      "Environment :: Console",
                      "Intended Audience :: Developers",
                      "License :: OSI-Approved Open Source :: BSD License",
                      "Natural Language :: English",
                      "Operating System :: OS Independent",
                      "Programming Language :: Python",
                      "Topic :: Database"])
