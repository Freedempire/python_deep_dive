numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
directions = ['E', 'S', 'W', 'N']

# combined = []
# for i, n in enumerate(numbers):
#     combined.append(str(n) + directions[i % 4])

combined = [str(n) + directions[i % 4] for i, n in enumerate(numbers)]
print(combined)