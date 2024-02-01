# zip all 3 files together
from contextlib import contextmanager

# method 1
with open('file1.txt') as f1, open('file2.txt') as f2, open('file3.txt') as f3: # with can open more than one context manager
    zipped_files = zip(f1, f2, f3)
    for row in zipped_files:
        print(row)
print('=' * 60)

# method 2
with open('file1.txt') as f1: # with can be nested
    with open('file2.txt') as f2:
        with open('file3.txt') as f3:
            zipped_files = zip(f1, f2, f3)
            for row in zipped_files:
                print(row)
print('=' * 60)

# the above methods cannot deal with arbitrary numbers of files

# method 3: modify the generator function to make it able to deal with indefinite numbers of files
@contextmanager
def open_files(filenames):
    if filenames:
        files = []
        for filename in filenames:
            files.append(open(filename))
        try:
            yield files
        finally:
            for file in files:
                file.close()
    else:
        yield None

filenames = 'file1.txt', 'file2.txt', 'file3.txt'
with open_files(filenames) as files:
    zipped_files = zip(*files)
    for row in zipped_files:
        print(row)
print('=' * 60)

# method 4: create a context manager to deal with other context managers
@contextmanager
def open_file(filename):
    file = open(filename)
    try:
        yield file
    finally:
        file.close()

class NestedContextManager:
    def __init__(self, *contexts):
        self._enters = []
        self._exits = []
        self._yields = []

        for context in contexts:
            self._enters.append(context.__enter__)
            self._exits.append(context.__exit__)

    def __enter__(self):
        for enter in self._enters:
            self._yields.append(enter())
        return self._yields

    def __exit__(self, exc_type, exc_value, traceback):
        for exit in self._exits[::-1]:
            exit(exc_type, exc_value, traceback)
        return False
    
filenames = 'file1.txt', 'file2.txt', 'file3.txt'
file_contexts = (open_file(filename) for filename in filenames)
with NestedContextManager(*file_contexts) as files:
    zipped_files = zip(*files)
    for row in zipped_files:
        print(row)
    