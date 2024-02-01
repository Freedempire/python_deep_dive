"""
Times how long a snippet of code takes to run over multiple iterations
"""

from time import perf_counter
from collections import namedtuple
import argparse

Timing = namedtuple('Timing', 'repeats elapsed average')

def timeit(source, repeats=10):
    code = compile(source, '<string>', 'exec')
    start = perf_counter()

    for _ in range(repeats):
        exec(code)

    elapsed = perf_counter() - start
    average = elapsed / repeats

    return Timing(repeats, elapsed, average)


if __name__ == '__main__':
    # get source, repeats from arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', # positinoal argument
                        type=str,
                        help='The Python source code to time.')
    parser.add_argument('-r', '--repeats', #option
                        type=int, default=10,
                        help='Number of times to repeat the test.')
    args = parser.parse_args()
    print(f'timing: {args.source}...')
    print(timeit(args.source, args.repeats))
