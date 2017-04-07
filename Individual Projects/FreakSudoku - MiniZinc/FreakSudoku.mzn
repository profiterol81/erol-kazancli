include "alldifferent.mzn";

% size of a box, this is also the number of boxes along a row or a cloumn
int: boxSize;
% size of a row and a column 
int: size = boxSize * boxSize;
% size of one side of the horizontal and vertical matrices
int: sizeComp = boxSize * (boxSize - 1);

array[1..size, 1..size] of var 1..size: sudoku;
array[1..size, 1..sizeComp] of string: horizontal;
array[1..sizeComp, 1..size] of string: vertical;

% all numbers are different in a column
constraint forall(r in 1..size) 
                    (alldifferent([sudoku[r, c] | c in 1..size]));
                        
% all numbers are different in a row                        
constraint forall(c in 1..size)  
                    (alldifferent([sudoku[r, c] | r in 1..size]));

% all numbers in boxes are different - foreach box the index starts from (b - 1) * boxSize 
constraint forall(b in 1..boxSize) 
                    (alldifferent([sudoku[(b - 1) * boxSize + r, (b - 1) * boxSize + c] | r in 1..boxSize, c in 1..boxSize]) );

% forall rows check the signs in the horizontal array to ensure the relationships in the matrix. Column c from the horizontal corresponds to c + ((c - 1) div 2) and c + ((c - 1) div 2) + 1 for comparison
constraint forall(r in 1..size) 
                    (forall(c in 1..sizeComp) 
                        (if horizontal[r, c] ==  ">" then sudoku[r, c + ((c - 1) div 2)] > sudoku[r, c + ((c - 1) div 2) + 1] 
                             else sudoku[r, c + ((c - 1) div 2)] < sudoku[r, c + ((c - 1) div 2) + 1] 
                         endif));

% forall columns check the signs in the vertical array to ensure the relationships in the matrix. Row r from the vertical corresponds to r + ((r - 1) div 2) and r + ((r - 1) div 2) + 1 for comparison
constraint forall(c in 1..size) 
                    (forall(r in 1..sizeComp) 
                        (if vertical[r, c] ==  "v" then sudoku[r + ((r - 1) div 2), c] > sudoku[r + ((r - 1) div 2) + 1, c] 
                            else sudoku[r + ((r - 1) div 2), c] < sudoku[r + ((r - 1) div 2) + 1, c] 
                         endif));

solve satisfy;

output [ show(sudoku[i,j]) ++ if j == size then "\n" else ", " endif | i in 1..size, j in 1..size];



    