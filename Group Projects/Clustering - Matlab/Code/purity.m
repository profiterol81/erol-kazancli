function [ purity_mat ] = purity( k, indexes,true_indexes )
%PURITY Summary of this function goes here
%   Detailed explanation goes here
purity_mat=zeros(k,1);
for i=1 : k
    cluster=indexes(true_indexes==i);
    purity_mat(i,1)=size(cluster(cluster==mode(cluster)),1)/size(cluster,1);
end

end

