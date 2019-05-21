import numpy as np
import sys
import CalculateTimeAndMedian as cm

sys.setrecursionlimit(50000)

nNumbers = 50000
ordered1 = np.fromfile('data/ordered1.dat', dtype=int);
ordered2 = np.fromfile('data/ordered2.dat', dtype=int);
ordered3 = np.fromfile('data/ordered3.dat', dtype=int);
ordered_with_repetition1 = np.fromfile('data/ordered_with_repetition1.dat', dtype=int);
ordered_with_repetition2 = np.fromfile('data/ordered_with_repetition2.dat', dtype=int);
ordered_with_repetition3 = np.fromfile('data/ordered_with_repetition3.dat', dtype=int);
reversed1 = np.fromfile('data/reversed1.dat', dtype=int);
reversed2 = np.fromfile('data/reversed2.dat', dtype=int);
reversed3 = np.fromfile('data/reversed3.dat', dtype=int);
reversed_with_repetitions1 = np.fromfile('data/reversed_with_repetitions1.dat', dtype=int);
reversed_with_repetitions2 = np.fromfile('data/reversed_with_repetitions2.dat', dtype=int);
reversed_with_repetitions3 = np.fromfile('data/reversed_with_repetitions3.dat', dtype=int);

ordered = np.zeros([3, nNumbers], dtype=int)
ordered[0] = ordered1
ordered[1] = ordered2
ordered[2] = ordered3

ordered_with_repetition = np.zeros([3, nNumbers], dtype=int)
ordered_with_repetition[0] = ordered_with_repetition1
ordered_with_repetition[1] = ordered_with_repetition2
ordered_with_repetition[2] = ordered_with_repetition3

reversed = np.zeros([3, nNumbers], dtype=int)
reversed[0] = reversed1
reversed[1] = reversed2
reversed[2] = reversed3

reversed_with_repetition = np.zeros([3, nNumbers], dtype=int)
reversed_with_repetition[0] = reversed_with_repetitions1
reversed_with_repetition[1] = reversed_with_repetitions2
reversed_with_repetition[2] = reversed_with_repetitions3

random = np.zeros([44, nNumbers], dtype=int)
random_with_rep = np.zeros([44, nNumbers], dtype=int)

for i in range(0, 44):
    random[i] = np.fromfile('data/random' + str(i) +'.dat', dtype=int);
for i in range(0, 44):
    random_with_rep[i] = np.fromfile('data/random_with_rep' + str(i) +'.dat', dtype=int);

print ("Ordered Data without Repetition:")
ordered_qsort = 0
ordered_rmedian = 0
ordered_qselect = 0
for i in range(0, 3):
    quick_sort_elapsed, r_median_elapsed, quick_select_elapsed, _ = cm.calculate(ordered[i])
    ordered_qsort += quick_sort_elapsed
    ordered_rmedian += r_median_elapsed
    ordered_qselect += quick_select_elapsed

print ("Ordered  Data with Repetition:")
ordered_wr_qsort = 0
ordered_wr_rmedian = 0
ordered_wr_qselect = 0
for i in range(0, 3):
    quick_sort_elapsed, r_median_elapsed, quick_select_elapsed, _ = cm.calculate(ordered_with_repetition[i])
    ordered_wr_qsort += quick_sort_elapsed
    ordered_wr_rmedian += r_median_elapsed
    ordered_wr_qselect += quick_select_elapsed

print ("Reverse Ordered Data without Repetition:")
reversed_qsort = 0
reversed_rmedian = 0
reversed_qselect = 0
for i in range(0, 3):
    quick_sort_elapsed, r_median_elapsed, quick_select_elapsed, _ = cm.calculate(reversed[i])
    reversed_qsort += quick_sort_elapsed
    reversed_rmedian += r_median_elapsed
    reversed_qselect += quick_select_elapsed

print ("Reverse Ordered Data with Repetition")
reversed_wr_qsort = 0
reversed_wr_rmedian = 0
reversed_wr_qselect = 0
for i in range(0, 3):
    quick_sort_elapsed, r_median_elapsed, quick_select_elapsed, _ = cm.calculate(reversed_with_repetition[i])
    reversed_wr_qsort += quick_sort_elapsed
    reversed_wr_rmedian += r_median_elapsed
    reversed_wr_qselect += quick_select_elapsed

print ("Random Data without Repetition:")
random_qsort = 0
random_rmedian = 0
random_qselect = 0
for i in range(0, 44):
    quick_sort_elapsed, r_median_elapsed, quick_select_elapsed, _ = cm.calculate(random[i])
    random_qsort += quick_sort_elapsed
    random_rmedian += r_median_elapsed
    random_qselect += quick_select_elapsed

print ("Random Data with Repetition:")
random_wr_qsort = 0
random_wr_rmedian = 0
random_wr_qselect = 0
for i in range(0, 44):
    quick_sort_elapsed, r_median_elapsed, quick_select_elapsed, _ = cm.calculate(random_with_rep[i])
    random_wr_qsort += quick_sort_elapsed
    random_wr_rmedian += r_median_elapsed
    random_wr_qselect += quick_select_elapsed

print ("Ordered Average:")
print ("Quick sort median time:" + str(ordered_qsort/3) + ", R median time:" + str(ordered_rmedian/3) + ", Quick Select median time:" + str(ordered_qselect/3))
print ("")
print ("Ordered With Repetition Average:")
print ("Quick sort median time:" + str(ordered_wr_qsort/3) + ", R median time:" + str(ordered_wr_rmedian/3) + ", Quick Select median time:" + str(ordered_wr_qselect/3))
print ("")
print ("Reversed Average:")
print ("Quick sort median time:" + str(reversed_qsort/3) + ", R median time:" + str(reversed_rmedian/3) + ", Quick Select median time:" + str(reversed_qselect/3))
print ("")
print ("Reversed With Repetition Average:")
print ("Quick sort median time:" + str(reversed_wr_qsort/3) + ", R median time:" + str(reversed_wr_rmedian/3) + ", Quick Select median time:" + str(reversed_wr_qselect/3))
print ("")
print ("Random Ordered Average:")
print ("Quick sort median time:" + str(random_qsort/44) + ", R median time:" + str(random_rmedian/44) + ", Quick Select median time:" + str(random_qselect/44))
print ("")
print ("Random with Repetition")
print ("Quick sort median time:" + str(random_wr_qsort/44) + ", R median time:" + str(random_wr_rmedian/44) + ", Quick Select median time:" + str(random_wr_qselect/44))
print ("")
avg_qsort = (ordered_qsort + ordered_wr_qsort + reversed_qsort + reversed_wr_qsort + random_qsort + random_wr_qsort) / 100
avg_rmedian = (ordered_rmedian + ordered_wr_rmedian + reversed_rmedian + reversed_wr_rmedian + random_rmedian + random_wr_rmedian) / 100
avg_qselect = (ordered_qselect + ordered_wr_qselect + reversed_qselect + reversed_wr_qselect + random_qselect + random_wr_qselect) / 100

print ("Quick sort median avg. time:" + str(avg_qsort) + ",  R median avg. time:" + str(avg_rmedian) + ", Quick Select median avg. time:" + str(avg_qselect))

