function plot_results( filename, data_mat,true_indexes,indexes, fuzzy_indexes, bisecting_indexes )
%PLOT_RESULTS Summary of this function goes here
%   Detailed explanation goes here

[feature_mat, eigenvalues, result]=my_pca(data_mat',3);
figure('Name', filename);

subplot(2,2,1)
c = true_indexes';
scatter3(result(:,1),result(:,2),result(:,3), 20, c, 'filled');
title('Original values');

subplot(2,2,2)
c = indexes';
scatter3(result(:,1),result(:,2),result(:,3), 20, c, 'filled');
title('K-means values');

subplot(2,2,3)
c = bisecting_indexes';
scatter3(result(:,1),result(:,2),result(:,3), 20, c, 'filled');
title('Bisecting K-means values');

subplot(2,2,4)
c = fuzzy_indexes';
scatter3(result(:,1),result(:,2),result(:,3), 20, c, 'filled');
title('Fuzzy C-means values');

[C_kmeans,order1] = confusionmat(true_indexes,indexes);
[C_fuzzy,order2] = confusionmat(true_indexes,fuzzy_indexes);
[C_bisecting,order3] = confusionmat(true_indexes,bisecting_indexes);

fg = figure('Name', filename);

set(fg,'Position',[500 500 900 150]);
columnname =   order1;
rowname =   order1;
columnformat = {'numeric', 'numeric', 'numeric'}; 

uitable('Units','normalized','Position',...
        [0 0 0.30 0.8], 'Data', C_kmeans,... 
        'ColumnName', columnname,...
        'ColumnFormat', columnformat,...
        'RowName',rowname);     

uitable('Units','normalized','Position',...
        [0.30 0 0.30 0.8], 'Data', C_bisecting,... 
        'ColumnName', columnname,...
        'ColumnFormat', columnformat,...
        'RowName',rowname); 


uitable('Units','normalized','Position',...
        [0.60 0 0.30 0.8], 'Data', C_fuzzy,... 
        'ColumnName', columnname,...
        'ColumnFormat', columnformat,...
        'RowName',rowname);     

uicontrol('Units','normalized', 'Style','text',...
'Position',[0 0.75 0.30 0.1],...
'String','Confusion Matrix - K Means');    

uicontrol('Units','normalized', 'Style','text',...
'Position',[0.30 0.75 0.30 0.1],...
'String','Confusion Matrix - Bisecting K Means');    

uicontrol('Units','normalized', 'Style','text',...
'Position',[0.60 0.75 0.30 0.1],...
'String','Confusion Matrix - Fuzzy C Means');    
        

end

