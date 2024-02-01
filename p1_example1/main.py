import sys

print(f'\n{'Running ' + __name__:=^80}\n')
print(sys.path)

from module1 import pprint_dict

pprint_dict('main.globals', globals())

print(f'\n{'End of ' + __name__:=^80}\n')