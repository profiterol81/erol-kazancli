function [CB,newClasses,samplesPerClass] = MaintenanceAlgorithmIB2( training_data, classes )
     dataSize = size(training_data, 1);
    
    CB=zeros(1,size(training_data,2));
    newClasses=zeros(1);
    for i=1:dataSize
        x=training_data(i,:);    
        sim=zeros(1,size(CB,1));
        for j=1:size(CB,1)
            
            y=CB(j,:);
            sim(j)=-findDistanceWithNominals(x,y);
            
        end
        if(~isequal(sim,zeros(1,size(CB,1))))
            found_class=newClasses(find(sim==max(sim)));
            true_class=classes(i);
            if(found_class~=true_class)
                CB=vertcat(CB, x);
                newClasses=vertcat(newClasses,true_class);
            end
        end
     
    end
CB=CB(any(CB,2),:);
newClasses=newClasses(any(CB,2),:);
uClasses=unique(classes);
samplesPerClass=zeros(1,length(uClasses));
for i=1:length(uClasses)
    samplesPerClass(i)=length(newClasses(newClasses==uClasses(i)));
end
