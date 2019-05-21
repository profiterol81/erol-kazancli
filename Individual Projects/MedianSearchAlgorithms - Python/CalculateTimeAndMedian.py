import QuickSort
import RMedian
import QuickSelect
import time
import math

def calculate(numbers):

    numbers1 = list(numbers)
    start = time.time()
    median_quick_sort = QuickSort.quick_sort_median(numbers1)
    end = time.time()

    quick_sort_elapsed = end - start

    numbers2 = list(numbers)
    start = time.time()
    success, median_r = RMedian.r_median_search(numbers2)
    end = time.time()

    r_median_elapsed = end - start

    numbers3 = list(numbers)
    start = time.time()
    median_quick_select = QuickSelect.quick_select(numbers3, math.ceil(len(numbers3)/float(2)), 0)
    end = time.time()

    quick_select_elapsed = end - start

    if median_r != median_quick_sort:
        print("R Median Fail")
    # print ("Quick sort:" + str(median_quick_sort) + ", R median:" + str(median_r) + ", Quick Select Median:" + str(median_quick_select) )
    # print ("Quick sort time:" + str(quick_sort_elapsed) + ", R median time:" + str(r_median_elapsed) + ", Quick Select median time:" + str(quick_select_elapsed))
    # print ("")
    return  quick_sort_elapsed, r_median_elapsed, quick_select_elapsed, success

