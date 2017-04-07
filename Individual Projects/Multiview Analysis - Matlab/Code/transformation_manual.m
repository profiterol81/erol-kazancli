I1 = imread('llibre1.jpg');
I2 = imread('llibre2.jpg');

% This part is for hand-selection of features
% imshow(I1);
% [y1,x1] = ginput(4);
% imshow(I2);
% [y2,x2] = ginput(4);

% hand selected features
y1 = [184;185;572;563];
x1 = [118;177;152;257];
y2 = [125;130;564;561];
x2 = [133;194;131;195];

A = [0, 0, 0, -x1(1), -y1(1), -1, y2(1)*x1(1), y2(1)*y1(1);
       x1(1), y1(1), 1, 0, 0, 0, -x2(1)*x1(1), -x2(1)*y1(1);
       0, 0, 0, -x1(2), -y1(2), -1, y2(2)*x1(2), y2(2)*y1(2);
       x1(2), y1(2), 1, 0, 0, 0, -x2(2)*x1(2), -x2(2)*y1(2);
        0, 0, 0, -x1(3), -y1(3), -1, y2(3)*x1(3), y2(3)*y1(3);
       x1(3), y1(3), 1, 0, 0, 0, -x2(3)*x1(3), -x2(3)*y1(3);
       0, 0, 0, -x1(4), -y1(4), -1, y2(4)*x1(4), y2(4)*y1(4);
       x1(4), y1(4), 1, 0, 0, 0, -x2(4)*x1(4), -x2(4)*y1(4)
       ];
B = [-y2(1);x2(1);-y2(2);x2(2);-y2(3);x2(3);-y2(4);x2(4)];
   
H = [linsolve(A,B);1];
H2 = reshape(H, 3, 3);

conI = uint8(zeros(size(I1, 1), size(I1, 2), size(I1, 3)));

% This part is for forward projection
% H2 = H2';
% for i = 1:size(I1, 1)
%     for j = 1:size(I1, 2)
%         coor1 = [i; j; 1];
%         coor2 = H2*coor1;
%         coor2 = coor2 / coor2(3);
%         if (round(coor2(1)) > 0 && round(coor2(2)) > 0 && round(coor2(1)) < size(conI, 1) && round(coor2(2)) < size(conI, 2))
%             conI(round(coor2(1)), round(coor2(2)), :) = I1(i, j, :);
%             
%         end    
%     end;
% end;  

% This part is for inverse projection
H2 = inv(H2');
for i = 1:size(I1, 1)
    for j = 1:size(I1, 2)
        coor1 = [i; j; 1];
        coor2 = H2*coor1;
        coor2 = coor2 / coor2(3);
        if (round(coor2(1)) > 0 && round(coor2(2)) > 0 && round(coor2(1)) < size(conI, 1) && round(coor2(2)) < size(conI, 2))
            conI(i, j, :) = I1(round(coor2(1)), round(coor2(2)), :);
            
        end    
    end;
end;  
imshow(conI);
imwrite(conI, 'llibre1Conv.jpg');




   


