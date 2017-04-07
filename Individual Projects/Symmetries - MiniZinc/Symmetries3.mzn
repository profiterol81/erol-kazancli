include "alldifferent.mzn";
include "globals.mzn";
int: gr; %number of groups
set of int: G=1..gr;
int: sz; %size of groups
set of int: S=1..sz;
int: n=gr*sz; %number of players
set of int: P=1..n;
int: we; % number of weeks
set of int: W=1..we;

array[G,W] of var set of P: X;

% every group has sz number of people
constraint forall(g in G) 
                  (forall(w in W)
                      (
                      (card(X[g, w]) ==  sz)
                      )
                  );
      
% no two people play in two different groups in different weeks                                 
constraint forall(w1 in W, w2 in W where w1 < w2)
                   (forall(g1 in G, g2 in G)
                        (
                        (card(X[g1, w1] intersect X[g2, w2]) <= 1)
                        )   
                   );    

% all groups have different people in a given week                   
constraint forall(w in W)
                   (forall(g1 in G, g2 in G where g1 < g2)
                        (
                        (card(X[g1, w] intersect X[g2, w]) == 0)
                        )   
                   );      

% break player symmetries                                       
constraint (forall(g in G)
                      (X[g, 1] = ((g-1)*sz + 1)..(g*sz))
                    );    

% Break group symmetries                         
constraint forall(w in W)
                   (forall(g1 in G, g2 in G where g1 < g2)
                        (
                        lex_greater([i in X[g1, w]| i in P], [i in X[g2, w]| i in P])
                        )   
                   );                     
                                        
%Break week symmetries                                                 
constraint forall(w1 in W, w2 in W where w1 < w2)
                        (
                        lex_greater([i in X[1, w1]| i in P], [i in X[1, w2]| i in P]) 
                        );                                                                                                                                                              
                                                                  
solve satisfy;   
                                 
% output [ show(X[i,j]) ++ if j == we then "\n" else ", " endif | i in   G, j in W];                                                               
output[""];                               