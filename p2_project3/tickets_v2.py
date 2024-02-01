from collections import namedtuple, defaultdict
from datetime import datetime
from functools import partial
from pprint import pprint


class Tickets:
    @staticmethod
    def parse_str(string, *, default=None):
        return string.strip() or default
    
    @staticmethod
    def parse_int(string, *, default=None):
        try:
            return int(string)
        except ValueError:
            return default
        
    @staticmethod
    def parse_date(string, *, default=None):
        try:
            return datetime.strptime(string.strip(), '%m/%d/%Y').date()
        except ValueError:
            return default

    @staticmethod
    def tickets_iterator(file):
        with open(file) as file:
            yield from file
        
    value_parsers = (
        parse_int, # the static method need to be defined before the reference to it
        lambda string: Tickets.parse_str(string, default=''), # need to use the class name to correctly reference the static method
        partial(parse_str, default=''), # same effect as above
        partial(parse_str, default=''),
        partial(parse_date, default=''),
        parse_int,
        partial(parse_str, default=''),
        partial(parse_str, default=''),
        partial(parse_str, default='')
    )

    @staticmethod
    def tickets_parser(file, *, default=None):
        ticket_rows = Tickets.tickets_iterator(file)
        headers = next(ticket_rows).strip().lower().replace(' ', '_').split(',')
        Ticket = namedtuple('Ticket', headers)
        for row in ticket_rows:
            # parse each item on the row
            data = list(parser(value) for parser, value in zip(Tickets.value_parsers, row.strip().split(',')))
            if all(item is not None for item in data): # check if any item is None, i.e. can't be parsed
                yield Ticket(*data)
            else:
                yield default


tickets = Tickets().tickets_parser('./nyc_parking_tickets_extract.csv')
tickets_list = list(tickets)
pprint(tickets_list[:5])
print(f'All tickets can be parsed (i.e. no None object in the list): {all(tickets_list)}')

# violations_by_make = {}
violations_by_make = defaultdict(int)
for ticket in tickets_list:
    # method 1, use setdefault
    # violations_by_make.setdefault(ticket.vehicle_make, 0)
    # violations_by_make[ticket.vehicle_make] += 1

    # method 2, use setdefault, combine two statements together
    # violations_by_make[ticket.vehicle_make] = violations_by_make.setdefault(ticket.vehicle_make, 0) + 1

    # method 3, use collections.defaultdict
    violations_by_make[ticket.vehicle_make] += 1 # if key doesn't exist, its value will be defaulted to 0

print(violations_by_make)
print(dict(sorted(violations_by_make.items(), key=lambda item: item[1], reverse=True)))
