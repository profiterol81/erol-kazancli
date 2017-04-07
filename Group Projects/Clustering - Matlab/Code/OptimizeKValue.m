function c = OptimizeKValue(filename, maxk)

    unnormalized_a=arffparser(filename);
    data_mat=normalizer(unnormalized_a);
    
    WGV = zeros(maxk);
    BGV = zeros(maxk);
    groups = 2:2+maxk-1;
    for i = 2 : 2 + maxk - 1
        [fuzzy_indexes, fuzzy_seeds, fuzzy_m, WGV(i - 1), BGV(i - 1)]=my_kmeans(data_mat, i);
    end
    
    figure('Name', 'Performance Index for K Values');

    subplot(2,2,1);
    plot(groups,WGV);
    
    xlabel('K');
    ylabel('Within Group Variance');
    
    subplot(2,2,2);
    plot(groups,BGV);
    xlabel('K');
    ylabel('Between Group Variance');
    
    subplot(2,2,3);
    plot(groups,WGV - BGV);
    xlabel('K');
    ylabel('WGV - BGV');


end        