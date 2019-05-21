import random

def quick_select(numbers, k, same_length):
    n = len(numbers)
    if n == 1 or same_length > 10:
        return numbers[0]
    r = random.randint(0, n - 1)
    pivot = numbers[r]

    s1 = []
    s2 = []
    for i in range(n):
        num = numbers[i]
        if num <= pivot:
            s1.append(num)
        else:
            s2.append(num)
    if len(s1)== 0 or len(s2) == 0:
        same_length += 1
    else:
        same_length = 0
    if k <= len(s1):
        return quick_select(s1, k, same_length)
    else:
        return quick_select(s2, k - len(s1), same_length)


