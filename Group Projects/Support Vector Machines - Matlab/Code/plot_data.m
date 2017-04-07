function plot_data( model, labels, data, my_title )

%we retrieve the training data belonging to each class
pos=data(:,labels==1);
neg=data(:,labels==-1);

x=data(1,:);

divisor =(-model.bias-model.weights(1,:)*x)/model.weights(2,:);
pos_vector=(-model.bias+1-model.weights(1,:)*x)/model.weights(2,:);
neg_vector=(-model.bias-1-model.weights(1,:)*x)/model.weights(2,:);

supportVectorPos=roundn((model.weights' * pos + model.bias),-3)<=1 & roundn((model.weights' * pos + model.bias),-3)>=-1;
supportVectorNeg=roundn((model.weights' * neg + model.bias),-3)>=-1 & roundn((model.weights' * neg + model.bias),-3)<=1;

figure;
scatter (pos(1,:),pos(2,:),'r');
hold on
scatter (neg(1,:),neg(2,:),'b');
scatter (pos(1,supportVectorPos),pos(2,supportVectorPos),'r', 'filled');
scatter (neg(1,supportVectorNeg),neg(2,supportVectorNeg),'b', 'filled');
plot (x,divisor, 'g'), title(my_title);
plot (x,pos_vector, 'r');
plot (x,neg_vector, 'b');
%axis([-0.6 0.4 -1 1])

hold off
end
