from collections import namedtuple


def cast_data(type_and_data):
    type_, data = type_and_data
    match type_:
        case 'STRING' | 'CAT':
            return str(data)
        case 'INT':
            return int(data)
        case 'DOUBLE':
            return float(data)
        case _:
            raise ValueError('Unknown type')

with open('./cars.csv') as file:
    headers = next(file).strip().split(';') # the file object itself is an iterator, so there's no need to call iter() on it
    data_types = next(file).strip().split(';')
    Car = namedtuple('Car', headers)
    # cars = []
    # for row in file:
    #     car = Car(*map(cast_data, zip(data_types, row.strip().split(';'))))
    #     cars.append(car)

    cars = [Car(*map(cast_data, zip(data_types, row.strip().split(';'))))
            for row in file]

print(cars)