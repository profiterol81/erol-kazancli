function [indexes,seeds,m] = bisecting_kmeans( data, k )
%BISECTING_KMEANS Summary of this function goes here
%   Detailed explanation goes here
num_clusters=1;
arr=data;
%arr=struct_to_matrix(data)';
indexes=ones(size(arr,1),1);
seeds = zeros (k, size(arr,2));

while num_clusters~=k
    % 1. Pick a cluster to split (largest)
    cluster=arr(indexes==mode(indexes),:);
    positions=find(indexes);
    positions=positions(indexes==mode(indexes));
    % 2. Find two subclusters using the basic k-Means algorithm(bisecting step)
    % 3. Repeat step 2 for n times and take the split that produces the
    % clustering with the highest overall similarity
    min_overall_distance=Inf;
    for i=1 : 5
        new_indexes=my_kmeans(cluster,2);
        combinations=nchoosek(find(cluster(:,1)),2);
        overall_distance=0;
        for j=1 : size(combinations,1 )
            overall_distance=overall_distance+(findDistance(cluster(combinations(j,1),:),cluster(combinations(j,2),:)));
        end
        if overall_distance < min_overall_distance
            min_overall_distance=overall_distance;
            clustering_indexes=new_indexes;
        end
    end
    clustering_indexes=clustering_indexes+max(unique(indexes));
    indexes(positions)=clustering_indexes;
    % 4. Repeat steps 1, 2 and 3 until the desired number of clusters is reached
    num_clusters=size(unique(indexes),1);
end
uniques=unique(indexes);
m = cell(k, 1);

for i=1 : k
    indexes(indexes==uniques(i,:))=i;
    m{i}=data(indexes==i,:);
    seeds(i, :) = mean(m{i}, 1);
end


end

