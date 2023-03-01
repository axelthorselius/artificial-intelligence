import numpy as np

x = np.array([1, 2, 3])

def check(x):
    return [1 if p > 1 else 0 for p in x]


print(check(x))
# print(x > 1)
