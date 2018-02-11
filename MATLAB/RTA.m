function [reg]=RTA(handles)
if ~isfield(handles,'int2')
    handles.int2=handles.int;
end
[layer,temp]=size(handles.int2);
if temp==3
    for i=1:layer
        handles.int2(i,4)=i;
    end  
end
[layer,temp]=size(handles.int);
if temp==3
    for i=1:layer
        handles.int(i,4)=i;
    end  
end
cla(handles.axes1);
cla(handles.axes2);
cla(handles.axes3);
global lambda_min;
global lambda_max;
global lambda_step;
global incident;
global materialA;
global materialB;
global substrate;
global impurity1;
global impurity2;
global reverse;
global angle;
global weight_spectra;
if isempty(angle), error('Please select angle');
end
ratio1=handles.int(:,1)/100;
ratio2=handles.int(:,2)/100;
if ratio1(end)==0 && ratio2(end)==0
    layer=layer-1;
end
if ratio1(end-1)==0 && ratio2(end-1)==0
    layer=layer-1;
end
Na = incident(:,1);  % first row is n, second row is k
Ka = incident(:,2);
Ns = substrate(:,1);
Ks = substrate(:,2);
%% Merit value part, create a filter, filt
filt=filtergenerate(handles);
%% n, k  row is each wavelength, column is material
Nar = ones(((lambda_max - lambda_min) / lambda_step) + 1, layer);
Kar = ones(((lambda_max - lambda_min) / lambda_step) + 1, layer);
for l = 1 : layer
    for wave = 1: (((lambda_max - lambda_min) / lambda_step) + 1)  
        if ratio1(l)>0.01 || ratio2(l)>0.01 
        Nar(wave, l) = materialA(wave,1)*ratio1(l) + materialB(wave, 1)*ratio2(l);
        Kar(wave, l) = materialA(wave,2)*ratio1(l) + materialB(wave, 2)*ratio2(l);
        else
        Nar(wave, l) = impurity1(wave,1)*ratio1(l) + impurity2(wave, 1)*ratio2(l);
        Kar(wave, l) = impurity1(wave,2)*ratio1(l) + impurity2(wave, 2)*ratio2(l);
        end
    end
end
legendcount=1;
%% calculate %R, %T, %A
if reverse ==1
    N=fliplr([Na Nar Ns]);
    K=fliplr([Ka Kar Ks]);
    thickness=flip(handles.int(:,3));
else
    N=[Na Nar Ns];
    K=[Ka Kar Ks];
    thickness=handles.int(:,3);
end
M= struct;
reflectivity=0;
transmissivity=1/1000;
for IA=angle;  % incident angle=0
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

    if length(angle)>1
        if IA==0
          set(handles.reftable,'Data',[(lambda_min:lambda_step:lambda_max)' rrtotal' tttotal' (100-rrtotal-tttotal)']);
          if get(handles.checkbox5,'value')~=1  %transfer function
                if get(handles.checkbox7,'Value')==1
                    mvalue=(1-tttotal)*filt(:,1);
                else 
                    mvalue=rrtotal*filt(:,1);
                end
            else
                if get(handles.checkbox7,'Value')==1
                    mvalue=abs((1-tttotal)-filt(:,1)').*filt(:,2)'*weight_spectra(:,1);
                else
                    mvalue=abs(rrtotal-filt(:,1)').*filt(:,2)'*weight_spectra(:,1);
                end
            end
        end
        axes(handles.axes1);
        plot(lambda_min:lambda_step:lambda_max,rrtotal);
        grid on;
        title('R%');
        xlabel('Wavelength(nm)');
        ylabel('Percent');
        hold on;
        legendInfo{legendcount} = ['Angle = ' num2str(IA)]; %
        legend(legendInfo);
        legendcount=legendcount+1;
    end
end
if length(angle)==1
    if get(handles.checkbox5,'value')~=1  %transfer function
        if get(handles.checkbox7,'Value')==1
            mvalue=(1-tttotal)*filt(:,1);
        else 
            mvalue=rrtotal*filt(:,1);
        end
    else
        if get(handles.checkbox7,'Value')==1
            mvalue=abs((1-tttotal)-filt(:,1)').*filt(:,2)'*weight_spectra(:,1);
        else
            mvalue=abs(rrtotal-filt(:,1)').*filt(:,2)'*weight_spectra(:,1);
        end
    end
    set(handles.reftable,'Data',[(lambda_min:lambda_step:lambda_max)' rrtotal' tttotal' (100-rrtotal-tttotal)']);
end
%% save in a register and plot
if handles.int(:,1:3)==handles.int2(:,1:3) %plot R% from file
        handles.reg.compare(:,3)=rrtotal'; % data from file
        handles.reg.mvalue(:,3)=mvalue;
        axes(handles.axes2);
        plot(lambda_min:lambda_step:lambda_max,handles.reg.compare(:,3));
        title('%R, Recipe from file');
        xlabel('Wavelength (nm)');
        ylabel('Percent');
        grid on;
        set(handles.o3,'String',num2str(handles.reg.mvalue(:,3)));
end
if length(angle)==1
    handles.reg.compare(:,2)=handles.reg.compare(:,1); % old data
    handles.reg.mvalue(:,2)=handles.reg.mvalue(:,1);
    handles.reg.compare(:,1)=rrtotal';  % new data
    handles.reg.mvalue(:,1)=mvalue;
    axes(handles.axes1);
    plot(lambda_min:lambda_step:lambda_max,handles.reg.compare(:,1),'b');
    hold on;
    plot(lambda_min:lambda_step:lambda_max,handles.reg.compare(:,2),'r');
    hold on;
    if  ~isempty(handles.wavm)   %load data
        xtemp=handles.wavm;
        ytemp=handles.refm;
        plot(xtemp,ytemp,'y');
        legend('Current R%', 'Last R%','Load R%');
    else
        legend('Current R%', 'Last R%');
    end
    grid on;
    set(gca,'xlim',[lambda_min lambda_max]);
    title('%R');
    xlabel('Wavelength (nm)');
    ylabel('Percent');
    hold off;
    set(handles.o2,'String',num2str(handles.reg.mvalue(:,2)));
    set(handles.o1,'String',num2str(handles.reg.mvalue(:,1)));  
else
    disp('If you want comparison, please select one angle');
end
%% 2-D projection
different=abs(handles.int2(:,3)-handles.int(:,3));
temp=sort(different);
svalue=temp(end-1:end);
if svalue(1)~=svalue(2)
    if svalue(1)~=0  % do projection
        pos1=handles.int2(find(different==svalue(1)),4);
        pos2=handles.int2(find(different==svalue(2)),4);
        projection(handles,pos1,pos2);
    end
end
reg=handles.reg;
end

