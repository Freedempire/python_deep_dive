files = ('./car-brands-1.txt', './car-brands-2.txt', './car-brands-3.txt')

def car_brands_generator(*files):
    for file in files:
        yield from clean_file(file)

def clean_file(file):
    with open(file) as f:
        for row in f:
            yield row.strip()


for car_brand in car_brands_generator(*files):
    print(car_brand)