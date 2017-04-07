function [model]= train_primal_soft_unbalanced (data,labels, lambda)
%TRAIN_PRIMAL primal problem for hard margin linear SVM


%we retrieve the training data belonging to each class
pos=data(labels==1,:)';
neg=data(labels==-1,:)';

cvx_begin
    %Variables
    variables w(2,1) b u(1,size(neg,2)) v(1,size(pos,2))
    %Function to minimize
    minimize( norm( w, 2 ) + lambda*(sum(u) + sum(v)*size(neg,2)/size(pos,2)))
    %subject to
    subject to
        %we want all negatives to be smaller than -1
        w'*neg + b <= -1 +u;
        %we want all positives to be bigger than 1
        w'*pos + b >= 1 -v;
        u>=0;
        v>=0;
cvx_end


model.weights=w;
model.bias=b;
model.u=u;
model.v=v;
