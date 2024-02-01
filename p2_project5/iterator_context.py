import csv
from collections import namedtuple
from pprint import pprint


def csv_generator(filename, tuplename):
    f = open(filename, newline='')
    dialect = csv.Sniffer().sniff(f.readline())
    f.seek(0)
    csv_reader = csv.reader(f, dialect)
    headers = map(lambda x: x.replace(' ', '_').lower(), next(csv_reader))
    named_tuple = namedtuple(tuplename, headers)
    try:
        yield (named_tuple(*row) for row in csv_reader)
    finally:
        f.close()

# class IteratorContextManager:
#     def __init__(self, generator):
#         self._generator = generator

#     def __enter__(self):
#         return next(self._generator)

#     def __exit__(self, exc_type, exc_value, traceback):
#         try:
#             next(self._generator)
#         except StopIteration:
#             pass
#         return False
    

class IteratorContextManager: # iterator and context manager at the same time
    def __init__(self, generator):
        self._generator = generator

    def __enter__(self):
        self._yielded = next(self._generator)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            next(self._generator)
        except StopIteration:
            pass
        return False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self._yielded)
    

# with IteratorContextManager(csv_generator('cars.csv', 'CarInfo')) as cars:
#     pprint(list(cars))

# combine the above iterator generator function and context manger together
# version 1
# class CsvParser: 
#     def __init__(self, filename, tuplename):
#         self._filename = filename
#         self._tuplename = tuplename

#     def __enter__(self):
#         self._generator = self.csv_generator()
#         self._yielded = next(self._generator)
#         return self

#     def __exit__(self, exc_type, exc_value, traceback):
#         try:
#             next(self._generator)
#         except StopIteration:
#             pass
#         return False

#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         return next(self._yielded)

#     def csv_generator(self):
#         csv_file = open(self._filename, newline='')

#         # detect dialect
#         dialect = csv.Sniffer().sniff(csv_file.readline())
#         csv_file.seek(0)

#         csv_reader = csv.reader(csv_file, dialect)

#         # get headers and create named tuple class
#         headers = map(lambda x: x.replace(' ', '_').lower(), next(csv_reader))
#         named_tuple = namedtuple(self._tuplename, headers)

#         try:
#             yield (named_tuple(*row) for row in csv_reader)
#         finally:
#             csv_file.close()


# version 2
class CsvParser:
    def __init__(self, filename, tuplename='Data'):
        self._filename = filename
        self._tuplename = tuplename

    def __enter__(self):
        self._file = open(self._filename, newline='')
        dialect = csv.Sniffer().sniff(self._file.readline())
        self._file.seek(0)
        self._csv_reader = csv.reader(self._file, dialect)
        headers = map(lambda x: x.replace(' ', '_').lower(), next(self._csv_reader))
        self._named_tuple = namedtuple(self._tuplename, headers)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._file.close()
        return False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._file.closed: # if iterator accessed from outside of with block, raise StopIteration instead of ValueError: I/O operation on closed file
            raise StopIteration
        else:
            return self._named_tuple(*next(self._csv_reader))

with CsvParser('personal_info.csv', 'PersonalInfo') as personals:
    pprint(list(personals))