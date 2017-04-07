%Main script for executing all the code in this assignment
clc;
close all;
clear;
disp('Introduction to Machine Learning');
disp('Universitat de Barcelona');
disp('Authors:')
disp('Erol Kazancli')
disp('Maria Leyva')
disp('W2: Adaptive Case-based reasoning exercise')
disp('Press any key to continue')
pause;

run('ReadDatasetsScript');

disp('Press any key to continue')
pause;

run('MaintenanceAlgorithmScript');

disp('Press any key to continue')
pause;

run('ACBRScript');

disp('Press any key to continue')
pause;

run('MaintainedACBRScript');

disp('Press any key to continue')
pause;

run('WeightedACBRScript');

disp('Press any key to finish and close all');
pause;
close all;
clc;
clear;

