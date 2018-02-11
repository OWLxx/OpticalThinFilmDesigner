function [ handles ] = control( handles )
%This is the control part of the GUI
% 2 weak prediction
% 3 strong prediction
% 4 two-layer ploting
% 5 RTA by recipe
% 6 RTA by coupling
global lambda_min;
global lambda_max;
global lambda_step;
global incident;
global materialA;
global materialB;
global substrate;
global factor;
global passband1;
global passband2;
global t_min;
global t_max;
global weight_spectra;
global runtime;
global impurity1;
global impurity2;
global Nooflayer;
global Noofgen;
global reverse;
global angle;
global transferfunction;
global sensitivity;
if get(handles.checkbox5,'Value')==1
    transferfunction=read_material_data(get(handles.tf,'String'));
end
if get(handles.checkbox6,'Value')==1
    sensitivity=str2double(get(handles.sen,'String'));
end
lambda_min=str2double(get(handles.minw,'String'));
lambda_max=str2double(get(handles.maxw,'String'));
lambda_step=str2double(get(handles.sc,'String'));
factor=str2double(get(handles.w,'String'));
passband1=str2double(get(handles.minp,'String'));
passband2=str2double(get(handles.maxp,'String'));
t_min=str2double(get(handles.mint,'String'));
t_max=str2double(get(handles.maxt,'String'));
incident=read_material_data(get(handles.in,'String'));   %should read material data
materialA=read_material_data(get(handles.c1,'String'));
materialB=read_material_data(get(handles.c2,'String'));
substrate=read_material_data(get(handles.s,'String'));
weight_spectra=read_material_data(get(handles.spec,'String'));
impurity1=read_material_data(get(handles.imp,'String'));
impurity2=read_material_data(get(handles.imp2,'String'));
Nooflayer=str2double(get(handles.nl,'String'));
Noofgen=str2double(get(handles.ng,'String'));
if get(handles.checkbox1,'value')==1
    reverse=1;
else 
    reverse=0;
end
if get(handles.checkbox2,'value')==1
    angletemp1=0;
else
    angletemp1=[];
end
if get(handles.checkbox3,'value')==1
    angletemp2=30;
else
    angletemp2=[];
end
if get(handles.checkbox4,'value')==1
    angletemp3=60;
else
    angletemp3=[];
end
angle=[angletemp1,angletemp2,angletemp3];
if runtime==1   % initializing something
    handles.reg.compare=zeros(((lambda_max-lambda_min)/lambda_step+1),3);
    handles.reg.mvalue=zeros(1,3);
    handles.wavm=[];
end

regi=struct;
switch get(handles.run,'Value')
    case 1 
        error('Please select a function');
    case 2  % generation algorithm
        handles=generationalgorithm(handles);
    case 3  % developing
         handles=boosting(handles);
    case 4
        twolayercoating(handles);
    case 5
        
        regi=RTA(handles);
        handles.reg=regi;
    case 6
        handles=plotdata(handles);
end
        
runtime=runtime+1;

end

