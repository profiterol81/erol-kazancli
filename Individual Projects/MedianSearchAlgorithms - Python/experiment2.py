import random as rd
import CalculateTimeAndMedian as cm
import sys

sys.setrecursionlimit(50000)

nNumbers = 50000
nDataSets = 1000
nFailures_rm = 0
total_qsort = 0
total_qselect = 0
total_rmedian = 0
for i in range(nDataSets):
    print ("Step " + str(i))
    dataset = [rd.randint(0, nNumbers) for r in xrange(nNumbers)]
    quick_sort_elapsed, r_median_elapsed, quick_select_elapsed, success_rm = cm.calculate(dataset)
    if success_rm == False:
        nFailures_rm += 1
    total_qsort +=  quick_sort_elapsed
    total_qselect += quick_select_elapsed
    total_rmedian += r_median_elapsed


print ("Number of failures from Random Median Out of 10000 trials: " + str(nFailures_rm))
print ("Quick sort median time:" + str(total_qsort/nDataSets) + ", R median time:" + str(total_rmedian/nDataSets) + ", Quick Select median time:" + str(total_qselect/nDataSets))
print ("")




