import argparse

parser = argparse.ArgumentParser(description='Print the squares of a list of numbers, and the cubes of another list')
parser.add_argument('-s', '--square', type=float, nargs='*', required=False, help='list of numbers to square')
parser.add_argument('-c', '--cube', type=float, nargs='+', required=True, help='list of numbers to cube')

args = parser.parse_args()

if args.square:
    print([n ** 2 for n in args.square])

print([n ** 3 for n in args.cube])