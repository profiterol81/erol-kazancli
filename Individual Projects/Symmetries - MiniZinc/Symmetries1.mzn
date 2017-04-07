include "alldifferent.mzn";
int: gr; %number of groups
set of int: G=1..gr;
int: sz; %size of groups
set of int: S=1..sz;
int: n=gr*sz; %number of players
set of int: P=1..n;
int: we; % number of weeks
set of int: W=1..we;

array[G,S,W] of var P: X;

% all players in a specific week are different
constraint forall(w in W) 
  (alldifferent([X[g, s, w] | g in G, s in S]));

%  no two players can play more than once in the same group  
constraint forall(w1 in W, w2 in W where w1 < w2)
                    (forall(g1 in G, g2 in G)
                        (forall(s11 in S, s12 in S where s11 < s12 )    
                            (forall(s21 in S, s22 in S)
                                  ((X[g1, s11, w1] != X[g2, s21, w2]) \/ (X[g1, s12, w1] != X[g2, s22, w2]))         
                            )    
                        )
                    );
 
% break player symmetries                                       
constraint (forall(g in G)
                       (forall (s in S)
                            (X[g, s, 1] = (g-1)*sz + s)
                       )
                    );                    

% Break in-group symmetries                    
constraint forall(w in W)
                    (forall(g in G)
                       (forall (s1 in S, s2 in 2..sz where s1 = s2 - 1)
                            (X[g, s1, w] < X[g, s2, w])
                       )
                    );
                    
% Break between group symmetries                    
constraint forall(w in W)
                    (forall(g1 in G, g2 in 2..gr where g1 = g2 - 1)
                         (X[g1, 1, w] < X[g2, 1, w])
                    );     

% Break week symmetries                   
constraint forall(w1 in W, w2 in 2..we where w1 = w2 - 1)                   
                         (X[1, 2, w1] < X[1, 2, w2]);                                                      
                    

% add people permutations                      
solve satisfy;                 

% output [ show(X[i,j,k]) ++ if k == we then "\n" else ", " endif | i in G, j in S, k in W];  
output[""];

  