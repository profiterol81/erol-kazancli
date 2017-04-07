function [ labels ] = test_primal_hard( model, data )
labels=zeros(size(data,2),1);

for i=1 : size(data,2)
    x=data(:,i);
    a=model.weights'*x +model.bias;
    if a>=0
        labels(i)=1;
    else
        labels(i)=-1;
    end
end
end

