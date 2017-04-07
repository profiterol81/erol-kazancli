function [rand_index, adjusted_rand_index] = rand_index( indexes, true_indexes )


a=0;
b=0;
c=0;
d=0;
for i=1 : size(indexes)
    for j=i : size(indexes)
        %AGREEMENTS
        %pairs of data that belong to the same cluster in indexes and
        %in matlab_indexes
        if indexes(i)==indexes(j)&& true_indexes(j)==true_indexes(i)
            a=a+1;
         %pairs of data that belong to different clusters in indexes and
        %in matlab_indexes
        elseif indexes(i)~=indexes(j)&& true_indexes(j)~=true_indexes(i)
            d=d+1;
        %DISAGREEMENTS      
         %pairs of data that belong to the same cluster in indexes
         %but not in matlab_indexes
        elseif indexes(i)==indexes(j)&& true_indexes(j)~=true_indexes(i)
            b=b+1;
        %pairs of data that belong to different clusters in indexes
         %but not in matlab_indexes
        elseif indexes(i)~=indexes(j)&& true_indexes(j)==true_indexes(i)
            c=c+1;
        end
    end
end

rand_index=(a+d)/(a+b+c+d);

%contigency matrix
cont_mat=crosstab(indexes, true_indexes);
%sums of rows
sum_rows=sum(cont_mat,2);
%sums of columns
sum_columns=sum(cont_mat,1);
total_comb=0;
for i=1 : size(cont_mat,1)
    for j=1 : size(cont_mat,2)
        n=cont_mat(i,j);
        if n>=2
            total_comb=total_comb+nchoosek(n,2);
        end
    end
end
comb_rows=0;
for i=1 : size(sum_rows,1)
    n=sum_rows(i,:);
    if n>=2
        comb_rows=comb_rows+nchoosek(n,2);
    end
end
comb_columns=0;
for i=1 : size(sum_columns,2)
    n=sum_columns(:,i);
    if n>=2
        comb_columns=comb_columns+nchoosek(n,2);
    end
end
expected_index=comb_columns*comb_rows/nchoosek(sum(sum_rows),2);
adjusted_rand_index=(total_comb-expected_index)/(0.5*(comb_columns+comb_rows)-expected_index);

end

