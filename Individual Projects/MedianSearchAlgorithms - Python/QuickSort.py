import math
import random as rd

def quick_sort_median(numbers):
    sorted_numbers = quicksort(numbers)
    return sorted_numbers[int(math.ceil(len(sorted_numbers)/float(2)) - 1)]

def quicksort(numbers):
    if len(numbers) <= 1:
        return numbers
    pivot = numbers[rd.randint(0, len(numbers) - 1)]
    first = []
    second = []
    middle = []
    for num in numbers:
        if num == pivot:
            middle.append(num)
        elif num > pivot:
            second.append(num)
        else:
            first.append(num)
    return quicksort(first) + middle + quicksort(second)
