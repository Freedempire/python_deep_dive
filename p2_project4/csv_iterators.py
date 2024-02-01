from csv import reader
from collections import namedtuple
from datetime import datetime, UTC
from functools import partial, reduce
from itertools import cycle, chain, groupby
# from itertools import islice, pairwise, starmap
from operator import add, eq
from pprint import pprint

def parse_str(string, *, default=None):
    if isinstance(string, str):
        if string:
            return string
        else:
            return default
    else:
        raise TypeError(f'string object expected, not {type(string).__name__}')
    
def parse_int(string, *, default=None):
    try:
        if isinstance(string, str):
            if string:
                return int(string)
            else:
                return default
        else:
            raise TypeError(f'string object expected, not {type(string).__name__}')
    except ValueError:
        return 'unparsable data'
    
def parse_datetime(string, format, *, default=None):
    try:
        if isinstance(string, str):
            if string:
                return datetime.strptime(string, format)
            else:
                return default
        else:
            raise TypeError(f'string object expected, not {type(string).__name__}')
    except ValueError:
        return 'unparsable data'

def csv_generator(filename, tuplename, *, delimiter=',', quotechar='"', parsers=[partial(parse_str, default='')]):
    with open(filename, newline='') as f:
        rows = reader(f, delimiter=delimiter, quotechar=quotechar)
        headers = next(rows)
        named = namedtuple(tuplename, headers)
        for row in rows:
            # if the elements in parsers are all the same parser, then parses can contain only one parser
            yield named(*(parser(field) for parser, field in zip(cycle(parsers), row)))

def is_compatible(namedtuples, keyname):
    # return all(starmap(eq, pairwise(map(lambda x: getattr(x, keyname), namedtuples))))
    # return all(getattr(nt, keyname) == getattr(namedtuples[0], keyname) for nt in namedtuples)
    return len(set(map(lambda x: getattr(x, keyname), namedtuples))) == 1

def combine_iterators(*iterators, keyname):
    initial_iteration = True
    zipped = zip(*iterators, strict=True)
    for namedts in zipped:
        if is_compatible(namedts, keyname): # check whether the value of SSN matches
            # combined_kvs = set(chain(*(namedt._asdict().items() for namedt in namedts))) # beware of set, the sequence may vary
            # combined_dict = dict(chain(*(namedt._asdict().items() for namedt in namedts))) # the order of dict is guaranteed, and duplicate elements are removed automatically same as set
            combined_dict = dict(chain.from_iterable((namedt._asdict().items() for namedt in namedts)))
            if initial_iteration:
                # Combined = namedtuple('Combined', (combined_kv[0] for combined_kv in combined_kvs))
                Combined = namedtuple('Combined', combined_dict)
                initial_iteration = False
                # yield Combined(**dict(combined_kvs))
            yield Combined(**combined_dict)
        else:
            raise ValueError(f'{keyname!r} between each iterable does not match, try sorting/cleaning data first')


employment_gen = csv_generator('./employment.csv', 'Employment', parsers=[parse_str])
personal_info_gen = csv_generator('./personal_info.csv', 'PersonalInfo', parsers=[parse_str])
update_status_gen = csv_generator('./update_status.csv',
                                  'UpdateStatus',
                                  parsers=[parse_str,
                                           partial(parse_datetime, format='%Y-%m-%dT%H:%M:%S%z'),
                                           partial(parse_datetime, format='%Y-%m-%dT%H:%M:%S%z')])
vehicles_gen = csv_generator('./vehicles.csv', 'Vehicle', parsers=[parse_str,
                                                                   parse_str,
                                                                   parse_str,
                                                                   parse_int])

# pprint(list(islice(employment_gen, 2)))
# pprint(list(islice(personal_info_gen, 2)))
# pprint(list(islice(update_status_gen, 2)))
# pprint(list(islice(vehicles_gen, 2)))

combined = combine_iterators(personal_info_gen, employment_gen, vehicles_gen, update_status_gen, keyname='ssn')
# pprint(list(islice(combined, 2)))

filtered_stales = filter(lambda record: record.last_updated < datetime(2017, 3, 1, tzinfo=UTC), combined)
# pprint(list(islice(filtered_stales, 2)))
# print(len(list(filtered_stales))) # 129

filtered_non_stales = filter(lambda record: record.last_updated >= datetime(2017, 3, 1, tzinfo=UTC), combined)
# print(len(list(filtered_non_stales))) # 871
non_stale_sorted = sorted(filtered_non_stales, key=lambda record: (record.gender, record.vehicle_make)) # sort by gender and vehicle_make at the same time
# pprint(non_stale_sorted)
vehicle_make_count_by_gender = {}
# for gender, gender_group in groupby(non_stale_sorted, lambda record: record.gender):
#     vehicle_make_count_by_gender[gender] = {vehicle_make: sum(1 for _ in record) for vehicle_make, record in groupby(gender_group, lambda record: record.vehicle_make)}

for k, g in groupby(non_stale_sorted, lambda record: (record.gender, record.vehicle_make)): # iterable can be grouped by complex key like sorted function
    vehicle_make_count_by_gender.setdefault(k[0], {})[k[1]] = sum(1 for _ in g)

# using loop to count is much simpler, easy to implement and no need to sort
# for record in filtered_non_stales:
#     vehicle_make_count_by_gender.setdefault(record.gender, {})
#     vehicle_make_count_by_gender[record.gender][record.vehicle_make] = vehicle_make_count_by_gender[record.gender].setdefault(record.vehicle_make, 0) + 1

pprint(vehicle_make_count_by_gender)