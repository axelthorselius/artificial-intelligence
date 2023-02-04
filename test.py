import sys
import numpy as np
import math

def main():
    # matrix = np.matrix([[0, 1, 2, 3, 4],
    #         [5,6,7,8,9],
    #         [10,11,12,13]])
    matrix = np.zeros((6, 7), dtype=int)
    sub_arr = matrix[:, 1]
    print(sub_arr)

if __name__ == '__main__':
    main()

