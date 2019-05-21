import random as rd
import numpy as np

nNumbers = 50000
ordered1 = np.arange(0, nNumbers).astype(int);
ordered1.tofile('data/ordered1.dat');
ordered2 = np.arange(10000, 10000 + nNumbers).astype(int);
ordered2.tofile('data/ordered2.dat');
ordered3 = np.arange(0, nNumbers * 5, 5).astype(int);
ordered3.tofile('data/ordered3.dat');
ordered_with_repetition1 = np.sort([rd.randint(0,nNumbers) for r in xrange(nNumbers)]).astype(int);
ordered_with_repetition1.tofile('data/ordered_with_repetition1.dat');
ordered_with_repetition2 = np.sort([rd.randint(20000, 20000 + nNumbers) for r in xrange(nNumbers)]).astype(int);
ordered_with_repetition2.tofile('data/ordered_with_repetition2.dat');
ordered_with_repetition3 = np.sort([rd.randint(1000,1100) for r in xrange(nNumbers)]).astype(int);
ordered_with_repetition3.tofile('data/ordered_with_repetition3.dat');
reversed1 = ordered1[::-1];
reversed1.tofile('data/reversed1.dat');
reversed2 = ordered2[::-1];
reversed2.tofile('data/reversed2.dat');
reversed3 = ordered3[::-1];
reversed3.tofile('data/reversed3.dat');
reversed_with_repetitions1 = ordered_with_repetition1[::-1];
reversed_with_repetitions1.tofile('data/reversed_with_repetitions1.dat');
reversed_with_repetitions2 = ordered_with_repetition2[::-1];
reversed_with_repetitions2.tofile('data/reversed_with_repetitions2.dat');
reversed_with_repetitions3 = ordered_with_repetition3[::-1];
reversed_with_repetitions3.tofile('data/reversed_with_repetitions3.dat');

for i in range(0, 15):
    rd.shuffle(ordered1)
    ordered1.tofile('data/random' + str(i) + '.dat');
    # ordered_random[i, :] = ordered1

for i in range(15, 30):
    rd.shuffle(ordered2)
    ordered2.tofile('data/random' + str(i) + '.dat');

for i in range(30, 44):
    rd.shuffle(ordered3)
    ordered2.tofile('data/random' + str(i) + '.dat');

for i in range(0, 15):
    rd.shuffle(ordered_with_repetition1)
    ordered_with_repetition1.tofile('data/random_with_rep' + str(i) + '.dat');

for i in range(15, 30):
    rd.shuffle(ordered_with_repetition2)
    ordered_with_repetition2.tofile('data/random_with_rep' + str(i) + '.dat');

for i in range(30, 44):
    rd.shuffle(ordered_with_repetition3)
    ordered_with_repetition3.tofile('data/random_with_rep' + str(i) + '.dat');

# np.savetxt("data/ordered_random_with_rep.txt", ordered_random);








#
#
# numbers = np.array([rd.randint(0,100000) for r in xrange(100000)])
# numbers.tofile('test2.dat')
# c = np.fromfile('test2.dat', dtype=int)