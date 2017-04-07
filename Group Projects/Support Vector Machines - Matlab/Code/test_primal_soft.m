function [ labels ] = test_primal_soft( model, data )
labels=zeros(size(data,1),1);

for i=1 : size(data,1)
    x=data(i,:)';
    a=model.weights'*x +model.bias;
    if a>=0
        labels(i)=1;
    else
        labels(i)=-1;
    end
end
end

