import random as rd
import math
import QuickSort

def r_median_search(numbers):
    subset = []
    n = len(numbers)
    pow = math.pow(n, float(3)/4)

    n_subset = int(math.ceil(pow))
    for i in range(n_subset):
        rn = rd.randint(0, len(numbers) - 1)
        subset.append(numbers[rn])

    subset = QuickSort.quicksort(subset)
    d = subset[int(math.floor(0.5 * pow - math.sqrt(n) - 1))]
    u = subset[int(math.floor(0.5 * pow + math.sqrt(n) - 1))]

    c = []
    lu = 0
    ld = 0
    for i in range(n):
        num = numbers[i]
        if num < d:
            ld += 1
        elif num > u:
            lu += 1
        else:
            c.append(num)

    success = False
    median = None
    if not(ld > n/2 or lu > n/2):
        if len(c) < 4 * pow:
            c = QuickSort.quicksort(c)
            median = c[int(math.ceil(n/float(2))) - ld - 1]
            success = True

    return success, median



