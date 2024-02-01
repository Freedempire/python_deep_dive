def pprint_dict(header, d):
    print(f'\n{header:-^60}')
    for k, v in d.items():
        print(f'{k}: {v}')
    print('-' * 60 + '\n')

print(f'\n{'Running ' + __name__:=^80}\n')

pprint_dict('module1.globals', globals())

print(f'\n{'End of ' + __name__:=^80}\n')