import os
from contextlib import contextmanager


@contextmanager
def temp_file(filename: str):
    try:
        yield filename
    finally:
        os.remove(filename)
