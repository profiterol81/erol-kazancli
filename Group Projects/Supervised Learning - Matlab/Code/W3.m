%Main script for executing all the code in this assignment
clc;
close all;
clear;
disp('Introduction to Machine Learning');
disp('Universitat de Barcelona');
disp('Authors:')
disp('Erol Kazancli')
disp('María Leyva')
disp('W3: A simple supervised problem')
disp('Press any key to continue')
pause;
disp('A:Data set analysis')
disp('Plotting the dataset');
run('Data_set_analysis');
disp('Press any key to continue')
pause;
clc;
clear;
close all;

disp('B. Analytical solution for the linear regression method.');
run('Analytical_solution');
disp('Press any key to continue')
pause;

clc;
close all;
clear;
disp('C. Linear regression and descent method.');
run('Linear_regression_and_descent_method');
disp('Press any key to continue')
pause;

clc;
close all;
clear;
disp('D. A second model.');
run('polynomial_model_analysis');
disp('Press any key to continue')
pause;

clc;
close all;
clear;
disp('E. Evaluating a model.');
run('model_evaluation');
disp('Please take a look to the displayed figures');
disp('Press any key to finish and close all')
pause;
close all;
clear;
clc;