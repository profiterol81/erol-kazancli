function clustering_analysis(filenames, numIterations)
    kmeans_data=zeros(size(filenames,1),4);
    bisecting_kmeans_data=zeros(size(filenames,1),4);
    fuzzy_data=zeros(size(filenames,1),4);
    max_k=1;
    
    for f=1 :size(filenames,1)
        
        filename=filenames{f};
        unnormalized_a=arffparser(filename);
        data_mat=normalizer(unnormalized_a);
        
        k=size(unnormalized_a.class.kind, 2);
        rand_index_mat=zeros(1,5);
        adjusted_rand_index=zeros(1,5);
        davies_boldin=zeros(1,5);

        fuzzy_rand_index_mat=zeros(1,5);
        fuzzy_adjusted_rand_index=zeros(1,5);
        fuzzy_davies_boldin=zeros(1,5);

        bisecting_rand_index_mat=zeros(1,5);
        bisecting_adjusted_rand_index=zeros(1,5);
        bisecting_davies_boldin=zeros(1,5);
        
        dataSize = size(data_mat,1);

        % purity=zeros(1,3);
        true_indexes=zeros(dataSize,1);
        
        for i=1 :k
            if iscell(unnormalized_a.class.kind)
                class=unnormalized_a.class.kind{i};
                true_indexes(strcmp(unnormalized_a.class.values,class))=i;
            else
                class=unnormalized_a.class.kind(i);
                true_indexes(unnormalized_a.class.values == class)=i;
            end    
        end
        
        fmeasure=zeros(k,5);
        fuzzy_fmeasure=zeros(k,5);
        bisecting_fmeasure=zeros(k,5);
        purity_mat=zeros(k,5);
        fuzzy_purity=zeros(k,5);
        bisecting_purity=zeros(k,5);

        %We repeat the estimations a number of times so that we get an average of
        %the indexes for each algorithm in the end
        for n = 1 : numIterations
            %Clustering
            [indexes, kmeans_seeds, kmeans_m]=my_kmeans(data_mat, k);
            [fuzzy_indexes, fuzzy_seeds,fuzzy_m]=fuzzycmeans(data_mat, k);
            [bisecting_indexes,bisecting_seeds,bisecting_m]=bisecting_kmeans(data_mat,k);
            
            [real_indexes] = findRealClasses(true_indexes, indexes, k);
            [real_fuzzy_indexes] = findRealClasses(true_indexes, fuzzy_indexes, k);
            [real_bisecting_indexes] = findRealClasses(true_indexes, bisecting_indexes, k);
            
            indexes = real_indexes;
            fuzzy_indexes = real_fuzzy_indexes;
            bisecting_indexes = real_bisecting_indexes;
            
            %Rand index and adjusted rand index
            [RI,ARI]=rand_index(indexes, true_indexes);
            rand_index_mat(1,n)=RI;
            adjusted_rand_index(1,n)=ARI;
            [RI,ARI]=rand_index(fuzzy_indexes, true_indexes);
            fuzzy_rand_index_mat(1,n)=RI;
            fuzzy_adjusted_rand_index(1,n)=ARI;
            [RI,ARI]=rand_index(bisecting_indexes,true_indexes);
            bisecting_rand_index_mat(1,n)=RI;
            bisecting_adjusted_rand_index(1,n)=ARI;
            %F-measure
            fmeasure(:,n)=f_measure(k,indexes,true_indexes);
            fuzzy_fmeasure(:,n)=f_measure(k,fuzzy_indexes,true_indexes);
            bisecting_fmeasure(:,n)=f_measure(k,bisecting_indexes,true_indexes);
            %Purity
            purity_mat(:,n)=purity(k,indexes,true_indexes);
            fuzzy_purity(:,n)=purity(k,fuzzy_indexes,true_indexes);
            bisecting_purity(:,n)=purity(k,bisecting_indexes,true_indexes);
            %Daves Boldin Index
            davies_boldin(1,n)= findDaviesBoldinIndex(kmeans_m, kmeans_seeds, k);
            fuzzy_davies_boldin(1,n)= findDaviesBoldinIndex(fuzzy_m, fuzzy_seeds, k);
            bisecting_davies_boldin(1,n)= findDaviesBoldinIndex(bisecting_m, bisecting_seeds, k);
        
        end
        
        plot_results(filenames{f}, data_mat,true_indexes,indexes, fuzzy_indexes, bisecting_indexes);       
     
        kmeans_data(f,1)=mean(rand_index_mat);
        kmeans_data(f,2)=mean(adjusted_rand_index);
        kmeans_data(f,3)=mean(davies_boldin);

        fuzzy_data(f,1)=mean(fuzzy_rand_index_mat);
        fuzzy_data(f,2)=mean(fuzzy_adjusted_rand_index);
        fuzzy_data(f,3)=mean(fuzzy_davies_boldin);

        bisecting_kmeans_data(f,1)=mean(bisecting_rand_index_mat);
        bisecting_kmeans_data(f,2)=mean(bisecting_adjusted_rand_index);
        bisecting_kmeans_data(f,3)=mean(bisecting_davies_boldin);
    
        if k > max_k
            prev_k = max_k;
            max_k=k;
            if prev_k ~= 1 
                intArr = zeros(size(filenames,1),max_k - prev_k);
                kmeans_data = [kmeans_data(:, 1:3+prev_k) intArr kmeans_data(:, 4+prev_k:3+2*prev_k) intArr];
                fuzzy_data = [fuzzy_data(:, 1:3+prev_k) intArr fuzzy_data(:, 4+prev_k:3+2*prev_k) intArr];
                bisecting_kmeans_data = [bisecting_kmeans_data(:, 1:3+prev_k) intArr bisecting_kmeans_data(:, 4+prev_k:3+2*prev_k) intArr];
            end
        end
        
        for g = 1 : size(fmeasure,1)
            
            kmeans_data(f, 3+g)=mean(fmeasure(g,:));
            kmeans_data(f, 3+max_k+g)=mean(purity_mat(g,:));

            fuzzy_data(f,3+g)=mean(fuzzy_fmeasure(g,:));
            fuzzy_data(f,3+max_k+g)=mean(fuzzy_purity(g,:));

            bisecting_kmeans_data(f,3+g)=mean(bisecting_fmeasure(g,:));
            bisecting_kmeans_data(f,3+max_k+g)=mean(bisecting_purity(g,:));

        end
    end
    
    header={'Rand index','Adjusted Rand Index','Davies-Bouldin Index'};
    
    for i = 1 : max_k
        header{3+i}=strcat('F-measure cluster ',num2str(i));
        header{3+max_k+i}=strcat('Purity cluster ',num2str(i));
    end
    
    header=sprintf('%s,',header{:},'');
    %header=strrep(header, ',', '');
    %header=strrep(header, ';', ',');
    dlmwrite('results/kmeans_analysis.csv',header,'');
    dlmwrite('results/kmeans_analysis.csv',kmeans_data,'-append');
    dlmwrite('results/fuzzycmeans_analysys.csv',header,'');
    dlmwrite('results/fuzzycmeans_analysys.csv',fuzzy_data, '-append');
    dlmwrite('results/bisectingkmeans_analysys.csv',header,'');
    dlmwrite('results/bisectingkmeans_analysys.csv',bisecting_kmeans_data, '-append');

end
