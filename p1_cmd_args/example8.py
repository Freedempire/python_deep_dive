import argparse
import cmath

parser = argparse.ArgumentParser(description='Test mutually exclusive arguments')
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
group.add_argument('-q', '--quiet', action='store_true', help='quiet mode')
parser.add_argument('number', type=complex, help='complex number')

# parser.add_argument('-a', '--age', default=20, type=int)
# parser.add_argument('name', default='Tony', nargs='?') # positioanl arguments with default values should have nargs set to ? or *

args = parser.parse_args()
# print(args)
number = args.number
if args.verbose:
    print('verbose mode...')
    print(f'input number: {number}')
    print(f'real part: {number.real}')
    print(f'imaginary part: {number.imag}')
    print(f'{number} = {cmath.polar(number)}')
elif args.quiet:
    print('quiet mode...')
    print('nothing to show here')
else:
    print('normal mode...')
    print(f'{number} = {cmath.polar(number)}')
