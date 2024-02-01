from collections import namedtuple

# method 1
def type_getter(type_str):
    match type_str:
        case 'STRING' | 'CAT':
            return str
        case 'INT':
            return int
        case 'DOUBLE':
            return float
        case _:
            raise ValueError('Unknown type')

# method 2
def cast_data(data_types):
    def inner(data):
        index, value = data
        match data_types[index]:
            case 'STRING' | 'CAT':
                return str(value)
            case 'INT':
                return int(value)
            case 'DOUBLE':
                return float(value)
            case _:
                raise ValueError('Unknown type')
    return inner
        
# method 3
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

cars = []

with open('./cars.csv') as file:
    index = 0
    for row in file:
        row = row.strip().split(';')
        if index == 0:
            Car = namedtuple('Car', row)
        elif index == 1:
            data_types = row
        else:
            # method 1
            # car = Car(*(type_getter(data_types[i])(value) for i, value in enumerate(row)))

            # method 2
            # car = Car(*map(cast_type(data_types), enumerate(row)))

            # method 3
            car = Car(*map(cast_data, zip(data_types, row)))
            cars.append(car)
        index += 1

print(cars)