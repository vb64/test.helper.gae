"""
pytest session setup
"""
import sys
import os
import pytest


def path_setup():
    """
    setup sys.path
    """
    cur_dir = os.getcwd()
    sys.path.insert(1, os.path.join(cur_dir, 'tests', 'gae'))


@pytest.fixture(scope="session", autouse=True)
def session_setup(request):
    """
    Auto session resource fixture
    """
    pass


path_setup()
