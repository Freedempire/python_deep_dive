def validate(data, template, prev_keys=None):
    if prev_keys is None:
        prev_keys = []
    for k, v in template.items():
        data_v = data.get(k, object()) # return default object() if k does not exist in data
        # if data_v != object(): # __eq__ of object is based on id, so it's always false
        if type(data_v) is not object:
            data_v_type = type(data_v)
            template_v_type = dict if isinstance(v, dict) else v
            if data_v_type is not template_v_type:
                prev_keys.append(k)
                return False, f'bad type: {'.'.join(prev_keys)}'
            else:
                if isinstance(v, dict):
                    prev_keys.append(k)
                    state, error = validate(data_v, v, prev_keys)
                    if not state:
                        return state, error
                    else:
                        prev_keys.pop() # remove the last previous key if state is True
        else:
            prev_keys.append(k)
            return False, f'mismatch keys: {'.'.join(prev_keys)}'
    return True, ''

template = {
    'user_id': int,
    'name': {
        'first': str,
        'last': str
    },
    'bio': {
        'dob': {
            'year': int,
            'month': int,
            'day': int
        },
        'birthplace': {
            'country': str,
            'city': str
        }
    }
}

john = {
    'user_id': 100,
    'name': {
        'first': 'John',
        'last': 'Cleese'
    },
    'bio': {
        'dob': {
            'year': 1939,
            'month': 11,
            'day': 27
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Weston-super-Mare'
        }
    }
}

eric = {
    'user_id': 101,
    'name': {
        'first': 'Eric',
        'last': 'Idle'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 3,
            'day': 29
        },
        'birthplace': {
            'country': 'United Kingdom'
        }
    }
}

michael = {
    'user_id': 102,
    'name': {
        'first': 'Michael',
        'last': 'Palin'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 'May',
            'day': 5
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Sheffield'
        }
    }
}

print(validate(john, template))
print(validate(eric, template))
print(validate(michael, template))