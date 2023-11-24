clc;
clear all;


input = imread('10.png'); 

output = underwater(input);

figure,imshow(input), title('original image');
figure,imshow(output),title('enhanced image');