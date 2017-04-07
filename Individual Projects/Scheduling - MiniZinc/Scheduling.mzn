include "cumulative.mzn";
include "globals.mzn";
include "alldifferent.mzn";
include "SchedulingExt.mzn";

int: c; %number of courses
int: g; %number of groups per course
int: nt; %number of theory rooms
int: nl; %number of laboratory rooms
int: d; % number of days
int: ini; %first available hour
int: end; %last available hour
array[1..c] of int: NT; %number of teachers per course

int: hoursPerDay = end - ini + 1; 
int: totalHours = hoursPerDay * d;

array[1..c, 1..g] of var 1..totalHours: startTheory;
array[1..c, 1..g] of var 1..totalHours: startLab;

array[1..160, 1..2] of 1..totalHours: order; % legitimate orders of theory-lab days

% symmetry: theory j always comes before theory k for group 1 if j < k
constraint forall(j in 1..c, k in 2..c where j + 1 = k) 
                      (
                         startTheory[j,1] < startTheory[k,1] 
                      );    

% symmetry: theory j always comes before theory k for course 1 if j < k
constraint forall(j in 1..g, k in 2..g where j + 1 = k) 
                      (
                         startTheory[1,j] < startTheory[1,k] 
                      );                                                

% alldifferent for non-overlap
constraint forall(i in 1..g)
                (alldifferent([startTheory[j,i] | j in 1..c] ++ [startLab[j,i] | j in 1..c]));
  
% cumulative for non-overlap
% constraint  forall(i in 1..g) % foreach group there can only be one lecture at any time - nonoverlap
%                   (
%                      cumulative([startTheory[j,i]| j in 1..c] ++ [startLab[j,i]| j in 1..c],[1| k in 1..c*2],[1| k in 1..c*2], 1)
%                   );     
    
% The three constraints below are an alternative to all-different non-overlap    
% constraint  forall(i in 1..g) % foreach group there can only be one lecture at any time - nonoverlap
%                   (
%                        forall(j in 1..c, k in 1..c where j != k) 
%                        (
%                           startTheory[j,i] != startTheory[k,i]
%                        )
%                   );
                  
% constraint  forall(i in 1..g) % foreach group there can only be one lecture at any time - nonoverlap
%                   (
%                        forall(j in 1..c, k in 1..c where j != k) 
%                        (
%                           startLab[j,i] != startLab[k,i]
%                        )
%                   );                                                       

% constraint  forall(i in 1..g) % foreach group there can only be one lecture at any time - nonoverlap
%                   (
%                        forall(j in 1..c, k in 1..c) 
%                        (
%                           startTheory[j,i] != startLab[k,i]
%                        )
%                   ); 

% Teacher constraint for each course
constraint  forall(i in 1..c) 
                  (
                     cumulative([startTheory[i,j]| j in 1..g] ++ [startLab[i,j]| j in 1..g],[1| k in 1..g*2],[1| k in 1..g*2], NT[i])
                  );

 % room constraint for theory
constraint cumulative([startTheory[i,j]| i in 1..c, j in 1..g], [1| i in 1..c*g],[1| i in 1..c*g], nt);

% room constraint for lab
constraint cumulative([startLab[i,j]| i in 1..c, j in 1..g], [1| i in 1..c*g],[1| i in 1..c*g], nl); 

% with table : for each course and group theory comes before lab and they should be on different days      
constraint forall(i in 1..c)  
                  (
                    forall(j in 1..g)
                    (
                      table([startTheory[i,j], startLab[i,j]], order)
                    )
                  );       
% without table : for each course and group theory comes before lab and they should be on different days                                                 
% constraint  forall(i in 1..c) 
%                   (
%                      forall(j in 1..g)
%                      (
%                          (startTheory[i,j] - 1) div hoursPerDay < (startLab[i,j] - 1) div hoursPerDay
%                       )
%                   );                  
solve satisfy;

output [ "Course" ++ show(i) ++ " Group" ++ show(j) ++ " Theory:" ++ show(startTheory[i,j]) ++ " Lab:" ++ show(startLab[i,j]) ++ if j == g then "\n" else ", " endif | i in 1..c, j in 1..g];