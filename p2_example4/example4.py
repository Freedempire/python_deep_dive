from itertools import groupby

with open('./cars_2014.csv') as f:
    next(f) # skip header row
    make_groups = groupby(f, lambda row: row.split(',')[0])
    model_count_by_make = {make: sum(1 for _ in group) for make, group in make_groups} # len() doesn't work on itertools._grouper

print(model_count_by_make)