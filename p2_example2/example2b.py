class CyclicIterator:
    def __init__(self, sequence):
        self._sequence = sequence
        self._index = 0

    def __len__(self):
        return len(self._sequence)

    def __iter__(self):
        return self
    
    def __next__(self):
        # if self._index >= len(self._sequence):
        #     self._index = 0
        # result = self._sequence[self._index]
        result = self._sequence[self._index % len(self)]
        self._index += 1
        return result


numbers = list(range(1, 14))
directions = 'ESWN'
directions_cyclic = CyclicIterator(directions)

print('[', end=' ')
for d in range(10):
    print(next(directions_cyclic), end=' ')
print(']')

# although the CyclicIterator has a finite length, it still causes an infinite for loop
# unless there is an extra length limit in the __next__ method
# for d in directions_cyclic:
#     print(d)

# use zip() and CyclicIterator
# combined = [f'{n}{d}' for n, d in zip(numbers, directions_cyclic)]

# use zip() and repeated iterable
# combined = [f'{n}{d}' for n, d in zip(numbers, 'ESWN' * (len(numbers) // len('ESWN') + 1))]

# use next() with CyclicIterator
combined = [f'{n}{next(directions_cyclic)}' for n in range(1, 14)]

print(combined)