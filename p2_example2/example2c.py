import itertools

# itertools.cycle(iterable)
# Make an iterator returning elements from the iterable and saving a copy of each.
# When the iterable is exhausted, return elements from the saved copy.
# Repeats indefinitely. Roughly equivalent to:
# def cycle(iterable):
#     # cycle('ABCD') --> A B C D A B C D A B C D ...
#     saved = []
#     for element in iterable:
#         yield element
#         saved.append(element)
#     while saved:
#         for element in saved:
#               yield element
# this implementation makes it not limited to sequence types unlike my CyclicIterator class

# itertools.zip_longest() is used to pad shorter iterables with a constant value

directions = 'ESWN'
combined = [f'{n}{d}' for n, d in zip(range(1, 14), itertools.cycle(directions))]
print(combined)