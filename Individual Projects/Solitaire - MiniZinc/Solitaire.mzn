include "globals.mzn";
include "alldifferent.mzn";
include "SolitaireExt.mzn";

int: s; %number of suits
int: m; %number of cards in each suit
int: sz=s*m; % size of the whole set
int: szPile; %size of the pile
int: numPile = ((sz - 1) div  szPile); % number of the piles 

array[1..numPile,1..szPile] of 2..sz: layout; % initial layout
array[1..sz] of var 1..sz: X; % the final stack
array[1..sz] of var 1..sz: Y; % the place of each card in the final stack
array[1..s] of string: types = ["Spade", "Club", "Diamond", "Heart"];

array[1..sz*s*2, 1..2] of 1..sz: order; % legitimate orders of two sequential cards

% The first card is 1 Spade
constraint X[1] == 1;

% X and Y are inverse of each other
constraint inverse(X, Y);    

% Only the top card in a pile can be moved in the next step
constraint  forall(i in 1..17)
                    (
                       forall (s1 in 1..2, s2 in 2..3 where s1 = s2 - 1)
                          (
                              Y[layout[i, s1]] < Y[layout[i, s2]]
                          )
                    ); 

% The next card can be one lower or one higher in rank - A table is used for allowable sequences                   
constraint forall(i in 1..51)
                  (
                    table([X[i], X[i+1]], order)
                  );                         
                       

solve satisfy;    

output [ show(X[i]) ++ "->" ++ show(((X[i]-1) mod 13) + 1) ++ "-" ++ show(types[((X[i] - 1) div m) + 1]) ++ "\n" | i in 1..sz];       
