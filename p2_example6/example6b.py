from contextlib import contextmanager

@contextmanager
def open_file(filename):
    file = open(filename)
    try:
        yield file
    finally:
        file.close()

class NestedContextManager:
    def __init__(self):
        self._exits = []

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        for exit in self._exits[::-1]:
            exit(exc_type, exc_value, traceback)
        return False
    
    def enter_context(self, context):
        self._exits.append(context.__exit__)
        return context.__enter__()
    
filenames = 'file1.txt', 'file2.txt', 'file3.txt'

with NestedContextManager() as stack:
    files = (stack.enter_context(open_file(filename)) for filename in filenames)
    for row in zip(*files):
        print(row)