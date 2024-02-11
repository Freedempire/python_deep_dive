class SchemaError(Exception):
    pass

class SchemaKeyMismatch(SchemaError):
    pass

class SchemaTypeMismatch(SchemaError, TypeError):
    pass

def validate(data, template, prev_keys=None):
    if prev_keys is None:
        prev_keys = []
    for k, v in template.items():
        data_v = data.get(k, object()) # return default object() if k does not exist in data
        if type(data_v) is not object:
            data_v_type = type(data_v)
            template_v_type = dict if isinstance(v, dict) else v
            if data_v_type is not template_v_type:
                prev_keys.append(k)
                raise SchemaTypeMismatch(f'bad type: {'.'.join(prev_keys)}')
            else:
                if isinstance(v, dict):
                    prev_keys.append(k)
                    validate(data_v, v, prev_keys)
                    prev_keys.pop() # remove the last previous key if no exception raises
        else:
            prev_keys.append(k)
            raise SchemaKeyMismatch(f'mismatch keys: {'.'.join(prev_keys)}')

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

tony = {
    'user_id': 103,
    'name': {
        'first': 'Tony',
        'last': 'King'
    },
    'bio': None
}

persons = [(john, 'John'), (eric, 'Eric'), (michael, 'Michael'), (tony, 'Tony')]

for person, name in persons:
    try:
        validate(person, template)
        print(f'{name}: ok')
    except SchemaError as e:
        print(f'{name}: {e.__repr__()}')

# result
# John: ok
# Eric: SchemaKeyMismatch('mismatch keys: bio.birthplace.city')
# Michael: SchemaTypeMismatch('bad type: bio.dob.month')
# Tony: SchemaTypeMismatch('bad type: bio')