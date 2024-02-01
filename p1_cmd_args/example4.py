import argparse

parser = argparse.ArgumentParser(description='Calculates div and mod of integers a and b')
parser.add_argument('a', type=int, help='integer a') # positional argument
parser.add_argument('b', type=int, help='integer b')

args = parser.parse_args()

a = args.a
b = args.b

print(f'a divmod b = {divmod(a, b)}')