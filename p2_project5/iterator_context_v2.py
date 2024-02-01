import csv
from collections import namedtuple
from contextlib import contextmanager
from pprint import pprint

@contextmanager
def csv_generator(filename, tuplename='Data'):
    file = open(filename, newline='')
    dialect = csv.Sniffer().sniff(file.readline())
    file.seek(0)
    csv_reader = csv.reader(file, dialect)
    headers = map(lambda x: x.replace(' ', '_').lower(), next(csv_reader))
    named_tuple = namedtuple(tuplename, headers)
    try:
        yield (named_tuple(*data) for data in csv_reader)
    finally:
        file.close()

with csv_generator('cars.csv') as cars:
    # print(next(cars))
    pprint(list(cars))
# print(next(cars)) # ValueError: I/O error raises here