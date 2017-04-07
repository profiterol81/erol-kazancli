
load('reg_data_set_1.mat')
%iterations
tau=1000;
%initial weights, theta
x = [ones(length(x),1) x];
theta = [0;0];
%learning rate, t
t=0.01;
disp('Parameters')
disp('Iterations')
disp(tau)
disp('Initial weights')
disp(theta);
disp('Learning rate')
disp(t);
%%Exercise C. Question block 3.
w_001=gradient_descent(x,y,theta,t,tau);

disp('Optimal weights')
disp(w_001);

disp('Press any key to continue')
pause;
%change t to 0.1 and repeat
disp('We change learning rate to 0.1');
t=0.1;
w_01=gradient_descent(x,y,theta,t,tau);

disp('Optimal weights')
disp(w_01);
disp('Press any key to continue')
pause;
%%Exercise C. Question block 4.
%Modified descent method
t=0.1;
tau=100;
disp('We modify the gradient desdent function');
disp('Parameters')
disp('Iterations')
disp(tau)
disp('Initial weights')
disp(theta);
disp('Learning rate')
disp(t);
modified_w=modified_gradient_descent(x,y,theta,t,tau);

disp('Optimal weights')
disp(modified_w);
%plot convergence part
