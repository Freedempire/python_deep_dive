import commons.validators as validators
import commons.models as models
# import commons.models.posts as posts
# from commons.models import *

print('\n\n*****self*****')
for k in list(globals()):
    print(k)

print('\n\n*****validators*****')
for k in validators.__dict__:
    print(k)

print('\n\n*****models*****')
for k in models.__dict__:
    print(k)

# print('\n\n*****posts*****')
# for k in posts.__dict__:
#     print(k)

print('\n\n*****numeric*****')
for k in validators.numeric.__dict__:
    print(k)

print('\n\n*****is_numeric*****')
print(validators.is_numeric)
