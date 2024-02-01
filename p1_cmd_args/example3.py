import sys

args_dict = {sys.argv[i]: sys.argv[i + 1] for i in range(1, len(sys.argv), 2)}
print(args_dict)

first_name = args_dict.get('--first-name', None)
last_name = args_dict.get('--last-name', None)
dob = args_dict.get('--dob', None)
print(first_name, last_name, dob)