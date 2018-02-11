function [ objvalue,int1 ] = meritcalc( pop, handles, flag )
%calculate merit value
%input row layer column thickness
%output vector, only merit value
if nargin<3
    flag=0;
end
if flag
    cla(handles.axes1);
    cla(handles.axes2);
end
[sx,sy]=size(pop);
layer=sy;
global lambda_min;
global lambda_max;
global lambda_step;
global incident;
global materialA;
global materialB;
global substrate;
global reverse;
global angle;
global sensitivity;
global weight_spectra;
if isempty(angle)
    angle=[0];
end
% calculate ratio
for i=1:2:sy
    ratio(i)=1;
end
for i=2:2:sy
    ratio(i)=0;
end
Na = incident(:,1);  % first row is n, second row is k
Ka = incident(:,2);
Ns = substrate(:,1);
Ks = substrate(:,2);
%% Merit value part, create a filter, filt
filt=filtergenerate(handles);
%% n, k for the two coating layer.  row is each wavelength, column is material
Nar = ones(((lambda_max - lambda_min) / lambda_step) + 1, layer);
Kar = ones(((lambda_max - lambda_min) / lambda_step) + 1, layer);
for l = 1 : layer
    for wave = 1: (((lambda_max - lambda_min) / lambda_step) + 1)
            Nar(wave, l) = materialA(wave,1)*ratio(l) + materialB(wave, 1)*(1-ratio(l));
            Kar(wave, l) = materialA(wave,2)*ratio(l) + materialB(wave, 2)*(1-ratio(l));
        
    end 
end
%% calculate %R, %T, %A
if reverse ==1
    N=fliplr([Na Nar Ns]);
    K=fliplr([Ka Kar Ks]);
else
    N=[Na Nar Ns];
    K=[Ka Kar Ks];
end
M= struct;
% for all the merit value of this pop
objvalue=zeros(1,sx);
legendInfo=cell(1);
for sample=1:sx
    if reverse==1
        thickness=fliplr(pop(sample,:))';
    else
        thickness=pop(sample,:)';
    end
    if get(handles.checkbox6,'value')==1
        thickness=thickness*(1+sensitivity*(rand-0.5)/50);
    end
    reflectivity=0;
    transmissivity=1/1000;
    legendcount=1;
    legendcount2=1;
    for IA=angle  % incident angle
        theta_i = IA*3.14/180 * ones(((lambda_max - lambda_min) / lambda_step) + 1, 1); %theta for first layer
        for i=1:layer+1  % include substrate layer  
            for wave = 1 : (((lambda_max - lambda_min) / lambda_step) + 1)
                theta_t(wave, i) = asin(N(wave, i)/N(wave, i+1) * sin(theta_i(wave, i)));  % T%
                theta_i(wave, i+1) = theta_t(wave, i); %i, incident refraction law R1*sin_theta1=R2*sin_theta2
                [M(wave, i).T, M(wave, i).TP] = x_matrix(theta_i(wave, i), theta_t(wave, i), N(wave, i), N(wave, i+1));
            end
        end
        rrtotal=zeros(1,((lambda_max - lambda_min) / lambda_step) + 1); % initialize
        tttotal=zeros(1,((lambda_max - lambda_min) / lambda_step) + 1); 
        l=1; % for count lambda
        for lambda=lambda_min: lambda_step: lambda_max   % calculate reflectance
        X_M=1;
        X_MP=1;
                     for i=1:layer % coating layer
                         M(l, i).P = [exp(-2*pi*(N(l, i+1)-K(l, i+1)*1i)*thickness(i)*cos(theta_t(l, i))/lambda*1i) 0; 0 exp(2*pi*(N(l, i+1) -K(l,i+1)*1i)*thickness(i)*cos(theta_t(l, i))/lambda*1i)]; 
                         X_M = M(l, i).P * M(l, i).T * X_M;
                         X_MP = M(l, i).P * M(l, i).TP * X_MP;    % P matrix in paper        
                     end
        X_M = M(l, layer+1).T * X_M;            % for interface with substrate
        X_MP= M(l, layer+1).TP * X_MP;

        rr(l)=abs(-X_M(2,1)/X_M(2,2));      % Reflection
        RR(l)=rr(l)^2*100;                  % Power, not wave,
        rrp(l)=abs(-X_MP(2,1)/X_MP(2,2));   % P polarization Reflection
        RRp(l)=rrp(l)^2*100; 
        if reverse==1
        tt(l)=abs(X_M(1,1)-X_M(2,1)*X_M(1,2)/X_M(2,2));
        TT(l)=(Ns(l)*cos(theta_i(1))) / (Na(l)*cos(theta_t(1))) * tt(l)^2*100;  %issue
        ttp(l)=abs(X_MP(1,1)-X_MP(2,1)*X_MP(1,2)/X_MP(2,2));
        TTp(l)=(Ns(l)*cos(theta_i(1))) / (Na(l)*cos(theta_t(1))) * ttp(l)^2*100;
        else
        tt(l)=abs(X_M(1,1)-X_M(2,1)*X_M(1,2)/X_M(2,2));
        TT(l)=(Na(l)*cos(theta_i(1))) / (Ns(l)*cos(theta_t(1))) * tt(l)^2*100;  %issue
        ttp(l)=abs(X_MP(1,1)-X_MP(2,1)*X_MP(1,2)/X_MP(2,2));
        TTp(l)=(Na(l)*cos(theta_i(1))) / (Ns(l)*cos(theta_t(1))) * ttp(l)^2*100;
        end
        %reflectivity=reflectivity + (RR(l) + R_weight(l)) + (RRp(l) + R_weight(l));
        reflectivity=reflectivity + RR(l) + (RRp(l));  % for total %R of all lambda, for merit value
        rrtotal(1,l)=(RR(l)+RRp(l))/2;  % R% for all wavelength
        transmissivity = transmissivity + TT(l) + TTp(l);
        tttotal(1,l)=(TT(l)+TTp(l))/2;  
        l=l+1;
        end
        if get(handles.checkbox5,'value')~=1  %transfer function           
             if get(handles.checkbox7,'Value')==1
                 objvalue(sample)=(1-tttotal)*filt(:,1)+objvalue(sample);
             else 
                 objvalue(sample)=rrtotal*filt(:,1)+objvalue(sample);
             end
        else
            
            if get(handles.checkbox7,'Value')==1
                 objvalue(sample)=abs((1-tttotal)-filt(:,1)').*filt(:,2)'*weight_spectra(:,1);
            else
                objvalue(sample)=abs(rrtotal-filt(:,1)').*filt(:,2)'*weight_spectra(:,1);
            end
        end
        if flag==1
            
            set(handles.rtable,'Data',[(ratio*100)', (100-ratio*100)', pop(1,:)']);
            int1=[(ratio*100)', (100-ratio*100)', pop(1,:)'];
            set(handles.reftable,'Data',[(lambda_min:lambda_step:lambda_max)', rrtotal', tttotal', (100-rrtotal-tttotal)']);
            axes(handles.axes1);
            plot(lambda_min:lambda_step:lambda_max,rrtotal);
            grid on;
            title('Best R%');
            xlabel('Wavelength (nm)');
            ylabel('Percent');
            hold on;
            legendInfo{legendcount} = ['Angle = ' num2str(IA)]; %
            legend(legendInfo);
            axes(handles.axes2);
            plot(lambda_min:lambda_step:lambda_max,tttotal);
            grid on;
            hold on;
            plot(lambda_min:lambda_step:lambda_max,100-rrtotal-tttotal);
            legendInfo2{legendcount2} = ['T% Angle = ' num2str(IA)];
            legendInfo2{legendcount2+1} = ['A% Angle = ' num2str(IA)];
            legend(legendInfo2);
            title('T% A%');
            xlabel('Wavelength (nm)');
            ylabel('Percent');
            legendcount=legendcount+1;
            legendcount2=legendcount2+2;
    
        end
    end    % end for angle
    
    
end


end

