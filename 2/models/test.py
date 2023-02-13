import random
# list = []

# list.append((1,2))
# list.append((3,4))

# print(len(list))
# print(list)

# i, j = None

# print(i)
# print(j)

move_list = [(1,2), (3,4), (5,6), None]
prob_list = [0.1, 0.1, 0.1, 0.7]

choice = random.choices(move_list, weights=prob_list, k=1)[0]
if choice != None:
    f, s = choice
    print(f)
    print(s)
else:
    print(choice)
