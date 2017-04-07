function [ error ] = weighted_error_rate( labels,my_labels )
pos=labels(labels==1);
my_pos=my_labels(labels==1);
pos_err=size(pos(pos~=my_pos),1);
neg=labels(labels==-1);
my_neg=my_labels(labels==-1);
neg_err=size(neg(neg~=my_neg),1);

error=(neg_err+pos_err*size(my_neg,1)/size(my_pos,1))/size(labels,1);
end

