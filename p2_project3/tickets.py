from collections import namedtuple
from datetime import date


class Tickets:
    @staticmethod
    def ticket_parser(file):
        ticket_rows = Tickets.tickets_iterator(file)
        headers = next(ticket_rows).strip().lower().replace(' ', '_').split(',')
        Ticket = namedtuple('Ticket', headers)
        for row in ticket_rows:
            data = row.strip().split(',')
            data[0] = int(data[0])
            # data[4] = datetime.datetime.strptime(data[4], '%m/%d/%Y').date()
            month, day, year = map(int, data[4].split('/')) # map returns an iterator, can be unpacked
            data[4] = date(year, month, day)
            data[5] = int(data[5])
            yield Ticket(*data)

    @staticmethod
    def tickets_iterator(file):
        with open(file) as file:
            yield from file


tickets = Tickets().ticket_parser('./nyc_parking_tickets_extract.csv')

violations_by_make = {}
for ticket in tickets:
    violations_by_make.setdefault(ticket.vehicle_make, 0)
    violations_by_make[ticket.vehicle_make] += 1

print(violations_by_make)
