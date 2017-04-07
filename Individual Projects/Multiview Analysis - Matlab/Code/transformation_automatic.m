Ia = imread('roofs2.jpg');
Ib = imread('roofs1.jpg');

I1 = single(rgb2gray(Ia));
I2 = single(rgb2gray(Ib));
[fa, da] = vl_sift(I1);
[fb, db] = vl_sift(I2);

[matches, scores] = vl_ubcmatch(da, db);

[B,I] = sort(scores);
A = matches(:, I);

% This part is to see the matching points
% show_keypoints(Ia,fa(:, A(1, 1:8)));
% figure;
% show_keypoints(Ib,fb(:, A(2, 1:8)));
% figure;
% show_matches(Ia,Ib,fa,fb,A(:, 1:8));

y1 = [fa(1, A(1, 1));fa(1, A(1, 2));fa(1, A(1, 3)); fa(1, A(1, 4)); fa(1, A(1, 5)); fa(1, A(1, 6)); fa(1, A(1, 7)); fa(1, A(1, 8))];
x1 = [fa(2, A(1, 1));fa(2, A(1, 2));fa(2, A(1, 3)); fa(2, A(1, 4)); fa(2, A(1, 5)); fa(2, A(1, 6)); fa(2, A(1, 7)); fa(2, A(1, 8))];
y2 = [fb(1, A(2, 1));fb(1, A(2, 2));fb(1, A(2, 3)); fb(1, A(2, 4)); fb(1, A(2, 5)); fb(1, A(2, 6)); fb(1, A(2, 7)); fb(1, A(2, 8))];
x2 = [fb(2, A(2, 1));fb(2, A(2, 2));fb(2, A(2, 3)); fb(2, A(2, 4)); fb(2, A(2, 5)); fb(2, A(2, 6)); fb(2, A(2, 7)); fb(2, A(2, 8))];

A = [0, 0, 0, -x1(1), -y1(1), -1, y2(1)*x1(1), y2(1)*y1(1);
       x1(1), y1(1), 1, 0, 0, 0, -x2(1)*x1(1), -x2(1)*y1(1);
       0, 0, 0, -x1(2), -y1(2), -1, y2(2)*x1(2), y2(2)*y1(2);
       x1(2), y1(2), 1, 0, 0, 0, -x2(2)*x1(2), -x2(2)*y1(2);
        0, 0, 0, -x1(3), -y1(3), -1, y2(3)*x1(3), y2(3)*y1(3);
       x1(3), y1(3), 1, 0, 0, 0, -x2(3)*x1(3), -x2(3)*y1(3);
       0, 0, 0, -x1(4), -y1(4), -1, y2(4)*x1(4), y2(4)*y1(4);
       x1(4), y1(4), 1, 0, 0, 0, -x2(4)*x1(4), -x2(4)*y1(4);
       0, 0, 0, -x1(5), -y1(5), -1, y2(5)*x1(5), y2(5)*y1(5);
       x1(5), y1(5), 1, 0, 0, 0, -x2(5)*x1(5), -x2(5)*y1(5);
       0, 0, 0, -x1(6), -y1(6), -1, y2(6)*x1(6), y2(6)*y1(6);
       x1(6), y1(6), 1, 0, 0, 0, -x2(6)*x1(6), -x2(6)*y1(6);
       0, 0, 0, -x1(7), -y1(7), -1, y2(7)*x1(7), y2(7)*y1(7);
       x1(7), y1(7), 1, 0, 0, 0, -x2(7)*x1(7), -x2(7)*y1(7);
       0, 0, 0, -x1(8), -y1(8), -1, y2(8)*x1(8), y2(8)*y1(8);
       x1(8), y1(8), 1, 0, 0, 0, -x2(8)*x1(8), -x2(8)*y1(8);
       
       ];
B = [-y2(1);x2(1);-y2(2);x2(2);-y2(3);x2(3);-y2(4);x2(4);-y2(5);x2(5);-y2(6);x2(6);-y2(7);x2(7);-y2(8);x2(8)];
   
H = [linsolve(A,B);1];
H2 = reshape(H, 3, 3);
H2 = inv(H2');

for i = 1:size(I1, 1)
    for j = 1:size(I1, 2)
        coor1 = [i; j; 1];
        coor2 = H2*coor1;
        coor2 = coor2 / coor2(3);
        X(i, j ,1) = round(coor2(1));
        X(i, j ,2) = round(coor2(2));  
    end;
end;  

% This min max is used since some parts of the original image stay out of
% the bounds, I increase the bounds
minY = min(min(X(:, :, 2)));
maxY = max(max(X(:, :, 2)));

X(:, :, 2) = X(:, :, 2) - minY + 1;
maxY = maxY - minY;

conI = uint8(zeros(size(Ia, 1), size(Ia, 2), 3));

for i = 1:size(conI, 1)
    for j = 1:size(conI, 2)
        if (X(i, j, 1) < size(Ia, 1) && X(i, j, 2) < size(Ia, 2) && X(i, j, 1) > 0 && X(i, j, 2) > 0)
            conI(i, j, :) = Ia(X(i, j, 1), X(i, j, 2), :);  
        end
    end;
end;  

imshow(conI);
imwrite(conI, 'roofs1Conv.jpg');


