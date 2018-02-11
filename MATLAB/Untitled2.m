clear all;clc;
ii=1
for seita=0:0.1:2*pi;
    A =[    1.2500   -0.2500;
       -0.2500    1.2500];
    B=[0.833 0.1667; 0.1667 0.83];

    P=[exp(-i*seita) 0; 0 exp(i*seita)];
    T=A*P*B;
    r(ii)=T(2,1)/T(1,1)
    R(ii)=abs(r(ii));
    ii=ii+1;
  
end
seita=0:0.1:2*pi;
  plot(seita,abs(r))
  xlabel('seita')
  ylabel('R')