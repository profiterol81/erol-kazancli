 function [feature_mat, eigenvalues, result, reconstructed_data] = my_pca(data, p)
% 1. Substract the mean from data
data_wo_mean=zeros(size(data));
avg=mean(data');
    for i = 1 : size(data,1)
    
        y = data(i,:);
        data_wo_mean(i,:)=data(i,:)-avg(i);
    end
 % 2. Calculate the covariance matrix
 cov_mat=cov(data_wo_mean');
% 3. Calculate the eigenvectors and eigenvalues of
% the covariance matrix
[eigenvectors,eigenvalues_mat]=eig(cov_mat);
eigenvalues=diag(eigenvalues_mat);
%order eigenvectors in decreasing value
[eigenvalues, indexes]=sort(eigenvalues*(-1));
eigenvectors=eigenvectors(:,indexes);
% 4. Choose components and construt a new feature vector
feature_mat=eigenvectors(:,1:p);
% 5. Derive the new data set
%TransformedData = RowFeatureVectAor × RowDataAdjust
result=zeros(size(data_wo_mean,1),size(feature_mat,2));
for i=1 : size(data_wo_mean,2)%563
    for j=1 : size(feature_mat,2) %4
        result(i,j)=feature_mat(:,j)'* data_wo_mean(:,i);
   % TransformedData(i)=feature_mat(:,i) * data_wo_mean(i);
    end
end
% 6. Reconstruct the old data back
%we still have old data
reconstructed_data=data;
 end