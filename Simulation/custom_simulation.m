clc;

%desired position and orientation
p = [0; 0; 210];
a = 0;
b = 0;
y = 0;

a11 = cos(y)*cos(b);
a12 = (cos(y)*sin(b)*sin(a)) - (sin(y)*cos(a));
a13 = (cos(y)*sin(b)*cos(a)) + (sin(y)*sin(a));
a21 = sin(y)*cos(b);
a22 = (sin(y)*sin(b)*sin(a)) + (cos(y)*cos(a));
a23 = (sin(y)*sin(b)*cos(a)) - (cos(y)*sin(a));
a31 = -sin(b);
a32 = cos(b)*sin(a);
a33 = cos(b)*cos(a);

R = [a11 a12 a13; a21 a22 a23; a31 a32 a33];


%Punkter 
a1 = [-142.28; -47.5; 0];
a2 = [-112.28; -99.47; 0];
a3 = [112.28; -99.47; 0];
a4 = [142.28; -47.5; 0];
a5 = [30; 146.97; 0];
a6 = [-30; 146.97; 0];

b1 = [-97.61; 21.72; 0];
b2 = [-30; -95.39; 0];
b3 = [30; -95.39; 0];
b4 = [97.61; 21.72; 0];
b5 = [67.61; 73.68; 0];
b6 = [-67.61; 73.68; 0];



    %Calculate outputs
    s1 = p + R*b1 - a1;
    s2 = p + R*b2 - a2;
    s3 = p + R*b3 - a3;
    s4 = p + R*b4 - a4;
    s5 = p + R*b5 - a5;
    s6 = p + R*b6 - a6;
    
    length_s1 = sqrt(s1(1)^2 + s1(2)^2 + s1(3)^2);
    length_s2 = sqrt(s2(1)^2 + s2(2)^2 + s2(3)^2);
    length_s3 = sqrt(s3(1)^2 + s3(2)^2 + s3(3)^2);
    length_s4 = sqrt(s4(1)^2 + s4(2)^2 + s4(3)^2);
    length_s5 = sqrt(s5(1)^2 + s5(2)^2 + s5(3)^2);
    length_s6 = sqrt(s6(1)^2 + s6(2)^2 + s6(3)^2);

    X = [a1(1) s1(1)+a1(1) s2(1)+a2(1) a2(1) s2(1)+a2(1) s3(1)+a3(1) a3(1) s3(1)+a3(1) s4(1)+a4(1) a4(1) s4(1)+a4(1) s5(1)+a5(1) a5(1) s5(1)+a5(1) s6(1)+a6(1) a6(1) s6(1)+a6(1) s1(1)+a1(1)];
    Y = [a1(2) s1(2)+a1(2) s2(2)+a2(2) a2(2) s2(2)+a2(2) s3(2)+a3(2) a3(2) s3(2)+a3(2) s4(2)+a4(2) a4(2) s4(2)+a4(2) s5(2)+a5(2) a5(2) s5(2)+a5(2) s6(2)+a6(2) a6(2) s6(2)+a6(2) s1(2)+a1(2)];
    Z = [a1(3) s1(3)+a1(3) s2(3)+a2(3) a2(3) s2(3)+a2(3) s3(3)+a3(3) a3(3) s3(3)+a3(3) s4(3)+a4(3) a4(3) s4(3)+a4(3) s5(3)+a5(3) a5(3) s5(3)+a5(3) s6(3)+a6(3) a6(3) s6(3)+a6(3) s1(3)+a1(3)];
    
    plot3(X, Y, Z)
    xlabel('x [mm]')
    ylabel('y [mm]')
    zlabel('z [mm]')
   
    d1 = length_s1 - 207;
    d2 = length_s2 - 207;
    d3 = length_s3 - 207;
    d4 = length_s4 - 207;
    d5 = length_s5 - 207;
    d6 = length_s6 - 207; 

    %pause(0.01)
    
    %i= i + 1;
    
    %p(1) = p(1) + 0.04;
