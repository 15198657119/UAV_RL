from itertools import permutations
from itertools import combinations
from itertools import product

# print(list(permutations(range(300))))
# print(list(combinations([1, 0, 1], r=1)))
import numpy as np

type = list(product(range(2), repeat=6))
print(type)
s = ('a', 'b', 'c')

# print(type)

sets = []
for t in type:
    for ss in s:
        sets.append((t, ss))

sets
