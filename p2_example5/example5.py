# pattern: change / reset
import sys

class OutToFile:
    def __init__(self, filename):
        self._filename = filename
        self._original_stdout = sys.stdout

    def __enter__(self):
        self._file = open(self._filename, 'w')
        sys.stdout = self._file
    
    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._original_stdout
        if not self._file.closed:
            self._file.close()
        return False

with OutToFile('test.txt'):
    print('Print something to the file')
    print('Print something more to the file')

print('Print something here')