function [ gestures,numG] = gestureCuts( X,Y)
% Input
% X: (T,80) skeletal frames.
% Y: (T,GN) 0/1 encoding of the gesture
%
% Output
% gestures: type of action time of each gesture divided
% ngestures: Number of gestures in the sequence
T=size(X,1);
gestures=ones(1,3);
numG=0;
ant=1;
for ti=1:T
    if(sum(Y(ti,:))>0)
        numG=numG+1;
        if(Y(ti,1)==1)
            gestures(numG,1)=1;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,2)==1)
            gestures(numG,1)=2;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,3)==1)
            gestures(numG,1)=3;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,4)==1)
            gestures(numG,1)=4;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,5)==1)
            gestures(numG,1)=5;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,6)==1)
            gestures(numG,1)=6;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,7)==1)
            gestures(numG,1)=7;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,8)==1)
            gestures(numG,1)=8;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,9)==1)
            gestures(numG,1)=9;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,10)==1)
            gestures(numG,1)=10;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,11)==1)
            gestures(numG,1)=11;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
        if(Y(ti,12)==1)
            gestures(numG,1)=12;
            gestures(numG,2)=ant;
            gestures(numG,3)=ti;
            ant=ti+5;
        end
    end

end

