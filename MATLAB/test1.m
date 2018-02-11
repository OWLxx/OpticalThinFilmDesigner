%test of general transfer-matrix method for optical multilayer...
% by Charalambos C.Katsidis 
clear all;
N1=1; N2=1.5; thetai=0; thetat=0;
t1 = 2*N1*cos(thetai)/(N1*cos(thetai)+N2*cos(thetat));
r1 = (N1*cos(thetai)-N2*cos(thetat))/(N1*cos(thetai)+N2*cos(thetat));
N2=1.2; N1=1.5; thetai=0; thetat=0;
t2 = 2*N1*cos(thetai)/(N1*cos(thetai)+N2*cos(thetat));
r2 = (N1*cos(thetai)-N2*cos(thetat))/(N1*cos(thetai)+N2*cos(thetat));
T1=(1/(t1^2)).*[1 -(r1.^2); r1^2 t1^2-r1^2];
T2=(1/(t2^2)).*[1 -(r2.^2); r2^2 t2^2-r2^2];
num=1;

TT=T1*T2
R=TT(2,1)/TT(1,1)
T=1/TT(1,1)

