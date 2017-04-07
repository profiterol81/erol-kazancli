include "globals.mzn";
int: gr; %number of groups
set of int: G=1..gr;
int: sz; %size of groups
set of int: S=1..sz;
int: n=gr*sz; %number of players
set of int: P=1..n;
int: we; % number of weeks
set of int: W=1..we;

array[P,W] of var G: X;
                  constraint forall(w in W)
                      (
                         global_cardinality([X[p, w]| p in P], [i | i in G], [sz | i in G]) 
                      );                     
                  
% no two people play in two different groups in different weeks                       
constraint forall(w1 in W, w2 in W where w1 < w2)
                   (forall(p1, p2 in P where p1 < p2)
                       (if X[p1, w1] == X[p2, w1] then X[p1, w2] != X[p2, w2] else 1==1 endif)
                   
                   );  
                   
% break player symmetries  
constraint forall(p in P) 
                  (
                  X[p ,1] == ((p-1) div sz) + 1 
                  );                                                                                                                               

% Break between group symmetries                    
constraint forall(w in W) 
                  (
                      (value_precede_chain([i | i in G], [X[p,w] | p in P]))
                  );     
                  
% Break week symmetries                                     
constraint forall(w1, w2 in W where w1 < w2)
                   (   
                   lex_greater([X[p,w2] | p in P], [X[p,w1] | p in P])
                  );                            
             
                      
solve satisfy;                 

% output [ show(X[i,j]) ++ if j == we then "\n" else ", " endif | i in P, j in W];  
output[""];
  