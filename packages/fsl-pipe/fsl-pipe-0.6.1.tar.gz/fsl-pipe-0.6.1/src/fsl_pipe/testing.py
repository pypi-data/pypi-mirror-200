"""Helper functions for testing."""
import os


def touch(path):
    """Create a new dummy file at path."""
    with open(path, 'a'):
        os.utime(path, None)