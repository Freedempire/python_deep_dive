from contextlib import ExitStack

filenames = 'file1.txt', 'file2.txt', 'file3.txt'

with ExitStack() as stack:
    files = [stack.enter_context(open(filename)) for filename in filenames]
    for row in zip(*files):
        print(row)