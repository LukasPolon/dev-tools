""" Module responsible for running the application.
    Functions:
        - run
"""

import sys

from click import echo

from tools.apache_search.src.cli.apache_search import apache_search


def run():
    """ Start the application and handle exceptions. """
    try:
        apache_search()
    except Exception:
        exc_type, exc_value, _ = sys.exc_info()
        echo('>> ERR >> {}: {}'.format(exc_type.__name__, exc_value))
