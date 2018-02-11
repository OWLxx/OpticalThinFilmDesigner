clear all;clc;
A =[    1.2500   -0.2500;
   -0.2500    1.2500];
B=[0.833 0.1667; 0.1667 0.833];
d=10000e-9;
ii=1
lamb=0:0.1e-9:1000e-9;
for lambda=0:0.1e-9:1000e-9
    
    seita=2*pi/lambda*1.5*d
    P=[exp(-i*seita) 0; 0 exp(i*seita)];
    T=A*P*B
    r=T(2,1)/T(1,1);
    R(ii)=abs(r)^2
    ii=ii+1;

end
plot(lamb,R)
xlabel('wavelength');
ylabel('R');
mR=tsmovavg(R','s',500,1);
hold on;
plot(lamb,mR)