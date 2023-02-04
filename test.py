import sys
import numpy as np
import math

# def nbr_in_a_row(list: list, piece: int):
#     """
#     returns the longest 
#     """
#     longest = 0
#     temp = 0
#     end_index = 0
#     for i in range(len(list)):
#         if list[i] == piece:
#             temp += 1
#         else:
#             longest = max(longest, temp)
#             temp = 0
#             end_index = i - 1
#         if (temp > longest):
#             longest = temp
#             # end_index = i
#         # longest = max(longest, temp)

#     # print(end_index)
#     return longest

def main():
    # list = [0, 1, 2, 3, 4, 5, 6, 7 ,8 ,9 ,10]
    # print(nbr_in_a_row(list, 1))
    # print(sys.maxsize)
    # list = [0] * 7
    # print(list)
    # print(np.argmax(list))
    value = sys.maxsize
    print(value)
    value += 1
    print(value)

    mval = math.inf
    print(mval)
    mval -= 1
    print(mval)

if __name__ == '__main__':
    main()

