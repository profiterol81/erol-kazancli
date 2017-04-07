int: m; % number of missions
int:  n; % number of persons

set of int: MISSION = 1..m;
set of int: PERSON =  1..n; 

array[MISSION] of var set of 1..n: mis; % array of missions containing set of persons 

array[MISSION] of PERSON: minPerInMis; % minimum number of persons for mission
array[MISSION] of PERSON: maxPerInMis; % maximum number of persons for mission 

array[PERSON] of MISSION: minMisForPer; % minimum number of missions per person
array[PERSON] of MISSION: maxMisForPer; % maximum number of missions per person

% intermediate variable for number of missions of each person
array[PERSON] of var 0..m: missionPerPerson = 
                        [sum(mission in MISSION)
                            (person in mis[mission]) | person in PERSON]; 
  
% intermediate variable for cardinality of each mission                                                       
array[MISSION] of var 1..n: cardMission = 
                        [card(mis[mission]) | mission in MISSION];                            
                                               
% for all missions the number of persons should be bigger than or equal to minimum and smaller than or equal to maximum   
constraint forall(mission in MISSION)
                    (cardMission[mission] >= minPerInMis[mission] /\ cardMission[mission] <= maxPerInMis[mission]);   
                    
% for all persons the number of missions should be bigger than or equal to minimum and smaller than or equal to maximum        
constraint forall(person in PERSON)
                    (missionPerPerson[person] >= minMisForPer[person] /\ missionPerPerson[person] <= maxMisForPer[person] );
 
% all pairs of missions have exactly one common person                                               
constraint forall(mission1, mission2 in MISSION where mission1 < mission2) 
                      (card(mis[mission1] intersect mis[mission2]) == 1);     
                                                                                              
solve satisfy;    

output [ "mission " ++ show(i) ++ ": " ++ show(mis[i]) ++ "\n" | i in MISSION];                                                                
                    
                    
                                                    