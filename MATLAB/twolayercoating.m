function [ handles ] = twolayercoating( handles )
%this function is for plotting two layer coating
%M. Claudia Troparevsky, Transfer-matrix formalism for the calculation of
%optical response in multilayer systems...
%OCA, 2010
cla(handles.axes1);
legend(handles.axes1,'hide');
global lambda_min;
global lambda_max;
global lambda_step;
global incident;
global materialA;
global materialB;
global substrate;
global t_min;
global t_max;
resolution=(t_max-t_min)/40;  % define resolution of 3-d plotting
ratio=[1 0]; %only two layer
Na = incident(:,1);  % first row is n, second row is k
Ka = incident(:,2);
Ns = substrate(:,1);
Ks = substrate(:,2);
%% Merit value part, create a filter, filt
filt=filtergenerate(handles);
%% n, k for the two coating layer.  row is each wavelength, column is material
Nar = ones(((lambda_max - lambda_min) / lambda_step) + 1, 2);
Kar = ones(((lambda_max - lambda_min) / lambda_step) + 1, 2);
for l = 1 : 2
    for wave = 1: (((lambda_max - lambda_min) / lambda_step) + 1)           
        Nar(wave, l) = materialA(wave,1)*ratio(l) + materialB(wave, 1)*(1-ratio(l));
        Kar(wave, l) = materialA(wave,2)*ratio(l) + materialB(wave, 2)*(1-ratio(l));
       
    end 
end
%% calculate %R, %T, %A
N=[Na Nar Ns];
K=[Ka Kar Ks];
M= struct;
t1c=1;
for t1=t_min:resolution:t_max
    t2c=1;
    for t2=t_min:resolution:t_max
        thickness=[t1 t2];
        reflectivity=0;
        transmissivity=1/1000;
        for IA=[0]  % incident angle=0
            theta_i = IA*3.14/180 * ones(((lambda_max - lambda_min) / lambda_step) + 1, 1); %theta for first layer
            for i=1:3  % four layer, three interface
                for wave = 1 : (((lambda_max - lambda_min) / lambda_step) + 1)
                   theta_t(wave, i) = asin(N(wave, i)/N(wave, i+1) * sin(theta_i(wave, i)));  % T%
                   theta_i(wave, i+1) = theta_t(wave, i); %i, incident refraction law R1*sin_theta1=R2*sin_theta2
                   [M(wave, i).T, M(wave, i).TP] = x_matrix(theta_i(wave, i), theta_t(wave, i), N(wave, i), N(wave, i+1));
                   % I matrix in the paper
                   %TM = [1/taf  raf/taf;  raf/taf  1/taf];
   %                 TMP = [1/tpaf  rpaf/tpaf;  rpaf/tpaf  1/tpaf];
                end
            end

 % angle part ends, propogation part, https://en.wikipedia.org/wiki/Transfer-matrix_method_(optics)     
             rrtotal=zeros(1,((lambda_max - lambda_min) / lambda_step) + 1); % initialize
             tttotal=zeros(1,((lambda_max - lambda_min) / lambda_step) + 1);  
             l=1; % for count lambda
             for lambda=lambda_min: lambda_step: lambda_max   % calculate reflectance
                 X_M=1;
                 X_MP=1;
                 for i=1:2 % coating layer
                     M(l, i).P = [exp(-2*pi*(N(l, i+1)-K(l, i+1)*1i)*thickness(i)*cos(theta_t(l, i))/lambda*1i) 0; 0 exp(2*pi*(N(l, i+1) -K(l,i+1)*1i)*thickness(i)*cos(theta_t(l, i))/lambda*1i)]; 
                     X_M = M(l, i).P * M(l, i).T * X_M;
                     X_MP = M(l, i).P * M(l, i).TP * X_MP;    % P matrix in paper        
                 end
                    X_M = M(l, 3).T * X_M;            % for interface with substrate
                    X_MP= M(l, 3).TP * X_MP;
                
                    rr(l)=abs(-X_M(2,1)/X_M(2,2));      % Reflection
                    RR(l)=rr(l)^2*100;                  % Power, not wave,
                    rrp(l)=abs(-X_MP(2,1)/X_MP(2,2));   % P polarization Reflection
                    RRp(l)=rrp(l)^2*100;    
                    tt(l)=abs(X_M(1,1)-X_M(2,1)*X_M(1,2)/X_M(2,2));
                    TT(l)=(Na(l)*cos(theta_i(1))) / (Ns(l)*cos(theta_t(1))) * tt(l)^2*100;  %issue
                    ttp(l)=abs(X_MP(1,1)-X_MP(2,1)*X_MP(1,2)/X_MP(2,2));
                    TTp(l)=(Na(l)*cos(theta_i(1))) / (Ns(l)*cos(theta_t(1))) * ttp(l)^2*100;
                    %reflectivity=reflectivity + (RR(l) + R_weight(l)) + (RRp(l) + R_weight(l));
                    reflectivity=reflectivity + RR(l) + (RRp(l));  % for total %R of all lambda, for merit value
                    rrtotal(1,l)=(RR(l)+RRp(l))/2;  % R% for all wavelength
                    transmissivity = transmissivity + TT(l) + TTp(l);
                    tttotal(1,l)=(TT(l)+TTp(l))/2;  
                    l=l+1;
             end
        end
        if get(handles.checkbox5,'value')~=1  %transfer function
            if get(handles.checkbox7,'Value')==1
                mvalue(t1c,t2c)=(1-tttotal)*filt(:,1);
            else 
                mvalue(t1c,t2c)=rrtotal*filt(:,1);
            end
        else
            if get(handles.checkbox7,'Value')==1
                mvalue(t1c,t2c)=abs((1-tttotal)-filt(:,1)').*filt(:,2)'*weight_spectra(:,1);
            else
                mvalue(t1c,t2c)=abs(rrtotal-filt(:,1)').*filt(:,2)'*weight_spectra(:,1);
            end
        end
        handles.mvalue(t1c,t2c)=mvalue(t1c,t2c);
        t2c=t2c+1;
    end
    t1c=t1c+1;
end
[a,b]=meshgrid(t_min:resolution:t_max,t_min:resolution:t_max);
axes(handles.axes1);
surf(a,b,mvalue);
xlabel(strcat(get(handles.c1,'String'), thickness));
ylabel(strcat(get(handles.c2,'String'), thickness));

end

