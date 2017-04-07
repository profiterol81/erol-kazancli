function [fmeasure] = f_measure(k, indexes,true_indexes )
%F_MEASURE Summary of this function goes here
%   Detailed explanation goes here
fmeasure=zeros(k,1);
for i=1 : k
    
     j=mode(indexes(true_indexes==i));
    true_positives=size(indexes(indexes==i & true_indexes==j),1);
    true_negatives=size(indexes(indexes~=i & true_indexes~=j),1);
    false_positives=size(indexes(indexes==i & true_indexes~=j),1);
    false_negatives=size(indexes(indexes~=i & true_indexes==j),1);
    if true_positives>0
        precision=true_positives/(true_positives+false_positives);
        recall=true_positives/(true_positives+false_negatives);
        fmeasure(i,1)=2*(precision*recall)/(precision+recall);
        
    end
end
end

