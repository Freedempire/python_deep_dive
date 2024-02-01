import argparse

parser = argparse.ArgumentParser(description='Test defaults and flags')
parser.add_argument('vocation') # positional arguments are required by default
parser.add_argument('--name', action='store') # options / flags, as their name indicated, are optional by default; store is the default action
parser.add_argument('--const', action='store_const', const='Python') # store the const value specified by const, default ot None when the option not used.
parser.add_argument('--age', default=18)
parser.add_argument('-v', '--verbose', action='store_const', const=True, default=False) # action and default together doing the thing as below
parser.add_argument('-q', '--quiet', action='store_true') # special cases of 'store_const' used for values True and False, with default values of False and True respectively.
args = parser.parse_args()

print(args)